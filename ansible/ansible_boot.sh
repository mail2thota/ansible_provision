#!/bin/bash

set -e

date

HOST_USER_NAME="root"
HOST_PASSWORD="baesystems"
FOREMAN_USER_NAME="admin"
FOREMAN_PASSWORD="4HFefKecSjn2i7Z8"
GIT_CHECKOUT_PATH="/root/checkout_contents"
AMBARI_PATH="${GIT_CHECKOUT_PATH}/ambari"
HDP_PATH="${GIT_CHECKOUT_PATH}/hdp/blueprints"
FOREMAN_CALLBACK_PATH="${GIT_CHECKOUT_PATH}/foreman_callback.py"
AMBARI_SERVER_ID="ambariserver"
AMBARI_AGENT_ID="ambariagent"
AMBARI_USER_NAME="admin"
AMBARI_PASSWORD="admin"
HDP_BLUEPRINT_FILE="hdp2.6-singlenode-blueprint.json"
HDP_HOST_CONFIG_FILE="hdp2.6-singlenode-hostconfig.json"
HDP_BLUEPRINT_NAME="single-node-hdfs2"


#generate and configure ssh key,thereby create the server groups in ansible hosts 
if [ -f ~/.ssh/bootstrap_rsa.pub ]; then
  rm -rf ~/.ssh/bootstrap_rsa*
  > ~/.ssh/known_hosts
fi
ssh-keygen -f ~/.ssh/bootstrap_rsa -t rsa -N ''
echo "generated bootstrap key in ~/.ssh"
> /etc/ansible/hosts
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/bootstrap_rsa &>/dev/null
server_count=0
agent_count=0
hammer --csv -u "${FOREMAN_USER_NAME}" -p "${FOREMAN_PASSWORD}" host list | grep -vi '^Id' | awk -F, {'print $5, $2'} | grep -vi '^$(hostname -i)' >> /etc/hosts
server_cardinality="1"
agent_cardinality="1"
while read -r foreman_config
do
	host_ip="$(cut -d ' ' -f 2 <<< "${foreman_config}")"
	hammer --csv -u "${FOREMAN_USER_NAME}" -p "${FOREMAN_PASSWORD}" host list | grep -vi '^Id' | awk -F, {'print $5, $2'}  > temp_hosts
	host_domain="$(cut -d ' ' -f 1 <<< "${foreman_config}")"
	echo "copying shh key into ${host_domain} domain"
	ssh-keyscan "${host_domain}" >>~/.ssh/known_hosts
	sshpass -p "${HOST_PASSWORD}" ssh-copy-id -i ~/.ssh/bootstrap_rsa.pub "${HOST_USER_NAME}"@"${host_domain}"
	scp temp_hosts "${HOST_USER_NAME}"@"${host_domain}":/etc
	ssh -n "${HOST_USER_NAME}"@"${host_domain}" "cat /etc/temp_hosts >> /etc/hosts"
        ssh -n "${HOST_USER_NAME}"@"${host_domain}" "rm -rf /etc/yum.repos.d/*"
	rm -rf temp_hosts
	host_domain_temp="$(cut -d '.' -f 1 <<< "${host_domain}")"
	if [[ $host_domain_temp == *"${AMBARI_SERVER_ID}"* ]];then
  
		host_domain_temp="${host_domain_temp}-${AMBARI_AGENT_ID}"
    fi

	server_group_id_groups="$(cut -d '-' -f 2- <<< "${host_domain_temp}")"

	for server_group_id in $(echo $server_group_id_groups | sed "s/-/ /g")
	do
		if [ $AMBARI_SERVER_ID == "${server_group_id}" ];then
                    if [ $server_count -gt 0 ];then
			   ambari_server_hdp+=","
                           server_cardinality="1+"
			fi
           		ambari_server_hdp+="{ \"fqdn\" : \"${host_domain}\" }"			
			ambari_server_domains[server_count++]="${host_domain}"
		fi
		if [ $AMBARI_AGENT_ID == "${server_group_id}" ];then
                    if [[ $server_group_id_groups != *"${AMBARI_SERVER_ID}"* ]];then
                    	if [ $agent_count -gt 0 ];then
			    ambari_agent_hdp+=","
                            agent_cardinality="1+"
			fi
			ambari_agent_hdp+="{ \"fqdn\" : \"${host_domain}\" }"
			ambari_agent_domains[agent_count++]="${host_domain}"
                    fi
		fi
		server_group_id="[${server_group_id}]"
		server_list_temp="${server_groups##*"${server_group_id}"}"
		existing_host_domains="$(cut -d '[' -f 1 <<< "${server_list_temp}")"
		if [[ $existing_host_domains != *"${host_domain}"* ]];then
			if [[ $server_groups == *"${server_group_id}"* ]]; then
				server_group_temp="${server_group_id}\n${host_domain}"
				server_groups="${server_groups/"$server_group_id"/$server_group_temp}"
			else
				server_groups+="\n\n${server_group_id}\n${host_domain}"
			fi
		fi
	done
done < <(hammer --csv -u "${FOREMAN_USER_NAME}" -p "${FOREMAN_PASSWORD}" host list | grep -vi '^Id' | awk -F, {'print $2, $5'} | grep -vi "^$(hostname -f)" )
echo "adding server groups into ansible host"
echo -e "${server_groups}" > /etc/ansible/hosts

#confgure the ansible callback plugin for foreman
echo "configuring the ansible callback plugin for foreman"
mkdir -p /usr/share/ansible/plugins/callback
sed -i '/callback_plugins/s/^#//g' /etc/ansible/ansible.cfg
sed -i '/bin_ansible_callbacks/s/^#//g' /etc/ansible/ansible.cfg
sed -i '/bin_ansible_callbacks/s/False/True/g' /etc/ansible/ansible.cfg
cp "${FOREMAN_CALLBACK_PATH}" /usr/share/ansible/plugins/callback/foreman_callback.py
sed -i 's/<FOREMAN_URL>/"https:\/\/localhost"/g' /usr/share/ansible/plugins/callback/foreman_callback.py
sed -i 's/<FOREMAN_SSL_CERT>/"\/var\/lib\/puppet\/ssl\/certs\/'$(hostname -f)'.pem"/g' /usr/share/ansible/plugins/callback/foreman_callback.py
sed -i 's/<FOREMAN_SSL_KEY>/"\/var\/lib\/puppet\/ssl\/private_keys\/'$(hostname -f)'.pem"/g' /usr/share/ansible/plugins/callback/foreman_callback.py
sed -i 's/<FOREMAN_SSL_VERIFY>/"0"/g' /usr/share/ansible/plugins/callback/foreman_callback.py

#execution of ambari playbooks
echo "executing ansible playbook for ambari"
cp -r "${AMBARI_PATH}" .
cd ambari
sed -i "s/<AMBARI_SERVER_ID>/${AMBARI_SERVER_ID}/g" playbooks/conf/ambari/ambari_server.yml
sed -i "s/<AMBARI_SERVER_ID>/${AMBARI_SERVER_ID}/g" roles/ambari_agent/defaults/main.yml
sed -i "s/<AMBARI_AGENT_ID>/${AMBARI_AGENT_ID}/g" playbooks/conf/ambari/ambari_agent.yml
ansible-playbook playbooks/conf/ambari/ambari_server.yml
ansible-playbook playbooks/conf/ambari/ambari_agent.yml
cd ..
cp -r  "${HDP_PATH}" .
cd blueprints
sed -i "s/<AMBARI_SERVER_DOMAINS>/${ambari_server_hdp}/g" "${HDP_HOST_CONFIG_FILE}"
sed -i "s/<AMBARI_AGENT_DOMAINS>/${ambari_agent_hdp}/g" "${HDP_HOST_CONFIG_FILE}"
sed -i "s/<HDP_BLUEPRINT_NAME>/${HDP_BLUEPRINT_NAME}/g" "${HDP_HOST_CONFIG_FILE}"
sed -i "s/<HDP_BLUEPRINT_NAME>/${HDP_BLUEPRINT_NAME}/g" "${HDP_BLUEPRINT_FILE}"
sed -i "s/<SERVER_CARDINALITY>/${server_cardinality}/g" "${HDP_BLUEPRINT_FILE}"
sed -i "s/<AGENT_CARDINALITY>/${agent_cardinality}/g" "${HDP_BLUEPRINT_FILE}"

#launch of hdp cluster
for ambari_server_domain in "${ambari_server_domains[@]}"
do
	curl -v -H "X-Requested-By: ambari" -X POST -u "${AMBARI_USER_NAME}":"${AMBARI_PASSWORD}" -d @"${HDP_BLUEPRINT_FILE}" --noproxy "${ambari_server_domain}" http://"${ambari_server_domain}":8080/api/v1/blueprints/"${HDP_BLUEPRINT_NAME}"

	curl -v -H "X-Requested-By: ambari" -X POST -u "${AMBARI_USER_NAME}":"${AMBARI_PASSWORD}" -d @"${HDP_HOST_CONFIG_FILE}" --noproxy "${ambari_server_domain}" http://"${ambari_server_domain}":8080/api/v1/clusters/"${HDP_BLUEPRINT_NAME}"
done
cd ..

date

