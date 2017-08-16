#!/bin/bash

HOST_USER_NAME="root"
HOST_PASSWORD="baesystems"
FTP_URL="ftp://192.168.116.130"
ANSIBLE_HADOOP_PATH="${FTP_URL}/pub/ansible-hadoop-master/*"
ANSIBLE_HDP_PATH="${FTP_URL}/pub/blueprints/*"
FOREMAN_CALLBACK_PATH="${FTP_URL}/pub/foreman_callback.py"
PROXY_URL="http://10.129.49.21:8080"
AMBARI_SERVER_ID="ambariservers"
AMBARI_AGENT_ID="ambariagents"
AMBARI_USER_NAME="admin"
AMBARI_PASSWORD="admin"

#generate and configure ssh key,thereby create the server groups in ansible hosts 
if [ ! -f ~/.ssh/bootstrap_rsa.pub ]; then
	ssh-keygen -f ~/.ssh/bootstrap_rsa -t rsa -N ''
    echo "generated bootstrap key in ~/.ssh"
	> /etc/ansible/hosts
else
	echo "bootstrap key exists in ~/.ssh"
fi
server_groups=$(awk '$1=$1' ORS='\\n' /etc/ansible/hosts)
server_count=0
agent_count=0
hammer --csv -u admin -p w4SfFSGpjZamRUe3 host list | grep -vi '^Id' | awk -F, {'print $5, $2'} | grep -vi "^$(hostname -i)" >> /etc/hosts
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/bootstrap_rsa
while read -r foreman_config
do
	host_ip="$(cut -d ' ' -f 2 <<< "${foreman_config}")"
	hammer --csv -u admin -p w4SfFSGpjZamRUe3 host list | grep -vi '^Id' | awk -F, {'print $5, $2'} | grep -vi "^$host_ip" > temp_hosts
	host_domain="$(cut -d ' ' -f 1 <<< "${foreman_config}")"
	echo "copying shh key into ${host_domain} domain"
	ssh-keyscan "${host_domain}" >>~/.ssh/known_hosts
	sshpass -p "${HOST_PASSWORD}" ssh-copy-id -i ~/.ssh/bootstrap_rsa.pub "${HOST_USER_NAME}"@"${host_domain}"
	ssh -n "${HOST_USER_NAME}"@"${host_domain}" "echo proxy=${PROXY_URL} >> /etc/yum.conf"
	scp temp_hosts "${HOST_USER_NAME}"@"${host_domain}":/etc
	ssh -n "${HOST_USER_NAME}"@"${host_domain}" "cat /etc/temp_hosts >> /etc/hosts"
	rm -rf temp_hosts
	server_group_id_groups="$(cut -d '-' -f 2- <<< "$(cut -d '.' -f 1 <<< "${host_domain}")")"
	for server_group_id in $(echo $server_group_id_groups | sed "s/-/ /g")
	do
		if [ $AMBARI_SERVER_ID == "${server_group_id}" ];then
		    if [ $server_count -gt 0 ];then
			   ambari_server_hdp+=","
			fi
            ambari_server_hdp+="{ \"fqdn\" : \"${host_domain}\" }"			
			ambari_server_domains[server_count++]="${host_domain}"
		fi
		if [ $AMBARI_AGENT_ID == "${server_group_id}" ];then
		    if [ $agent_count -gt 0 ];then
				ambari_agent_hdp+=","
			fi
			ambari_agent_hdp+="{ \"fqdn\" : \"${host_domain}\" }"
			ambari_agent_domains[agent_count++]="${host_domain}"
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
done < <(hammer --csv -u admin -p w4SfFSGpjZamRUe3 host list | grep -vi '^Id' | awk -F, {'print $2, $5'} | grep -vi "^$(hostname -f)" )
echo "adding server groups into ansible host"
echo -e "${server_groups}" > /etc/ansible/hosts


#confgure the ansible callback plugin for foreman
echo "configuring the ansible callback plugin for foreman"
sed -i '/callback_plugins/s/^#//g' /etc/ansible/ansible.cfg
sed -i '/bin_ansible_callbacks/s/^#//g' /etc/ansible/ansible.cfg
sed -i '/bin_ansible_callbacks/s/False/True/g' /etc/ansible/ansible.cfg
curl "${FOREMAN_CALLBACK_PATH}" -o /usr/share/ansible/plugins/callback/foreman_callback.py
sed -i 's/<FOREMAN_URL>/"https:\/\/localhost"/g' /usr/share/ansible/plugins/callback/foreman_callback.py
sed -i 's/<FOREMAN_SSL_CERT>/"\/var\/lib\/puppet\/ssl\/certs\/'$(hostname -f)'.pem"/g' /usr/share/ansible/plugins/callback/foreman_callback.py
sed -i 's/<FOREMAN_SSL_KEY>/"\/var\/lib\/puppet\/ssl\/private_keys\/'$(hostname -f)'.pem"/g' /usr/share/ansible/plugins/callback/foreman_callback.py
sed -i 's/<FOREMAN_SSL_VERIFY>/"0"/g' /usr/share/ansible/plugins/callback/foreman_callback.py



#execution of hadoop playbooks
echo "executing ansible playbook for hadoop"
wget -r -np -nH --cut-dirs=1 "${ANSIBLE_HADOOP_PATH}"
wget -r -np -nH --cut-dirs=1 "${ANSIBLE_HDP_PATH}"
cd ansible-hadoop-master
sed -i "s/<AMBARI_SERVER_ID>/${AMBARI_SERVER_ID}/g" playbooks/conf/ambari/ambari_server.yml
sed -i "s/<AMBARI_SERVER_ID>/${AMBARI_SERVER_ID}/g" playbooks/operation/ambari/setup.yml
sed -i "s/<AMBARI_SERVER_ID>/${AMBARI_SERVER_ID}/g" roles/ambari_agent/defaults/main.yml
sed -i "s/<AMBARI_AGENT_ID>/${AMBARI_AGENT_ID}/g" playbooks/conf/ambari/ambari_agent.yml
ansible-playbook playbooks/conf/ambari/ambari_server.yml
ansible-playbook playbooks/operation/ambari/setup.yml
ansible-playbook playbooks/conf/ambari/ambari_agent.yml
cd ..
rm -rf ansible-hadoop-master
cd blueprints
sed -i "s/<AMBARI_SERVER_DOMAINS>/${ambari_server_hdp}/g" hdp2.4-multinode-hostconfig.json
sed -i "s/<AMBARI_AGENT_DOMAINS>/${ambari_agent_hdp}/g" hdp2.4-multinode-hostconfig.json

for ambari_server_domain in "${ambari_server_domains[@]}"
do
	curl -v -H "X-Requested-By: ambari" -X POST -u "${AMBARI_USER_NAME}":"${AMBARI_PASSWORD}" -d @hdp2.4-blueprint-multinode.json --noproxy "${ambari_server_domain}" http://"${ambari_server_domain}":8080/api/v1/blueprints/multi-node-hdfs

	curl -v -H "X-Requested-By: ambari" -X POST -u "${AMBARI_USER_NAME}":"${AMBARI_PASSWORD}" -d @hdp2.4-multinode-hostconfig.json --noproxy "${ambari_server_domain}" http://"${ambari_server_domain}":8080/api/v1/clusters/multi-node-hdfs
done
cd ..
rm -rf blueprints



