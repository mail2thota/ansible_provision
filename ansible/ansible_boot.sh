#!/bin/bash

set -e

HOST_USER_NAME=${node_user:-root}
HOST_PASSWORD=${node_pass:-baesystems}
FOREMAN_USER_NAME=${username:-admin}
FOREMAN_PASSWORD=${password:-4HFefKecSjn2i7Z8}
AMBARI_SERVER_HOST_ID=${ambari_host_suffix:-ambariserver}
AMBARI_AGENT_HOST_ID=${ambari_agent_suffix:-ambariagent}
AMBARI_SERVER_ID=${ambari_master_group:-ambari_master}
AMBARI_AGENT_ID=${ambari_agent_group:-ambari_slave}
HDP_REPO_URL=${hdp_repo_url:-http://10.129.6.142/repos/HDP/HDP-2.6.2.0/centos7}
HDP_UTILS_REPO_URL=${hdp_utils_repo_url:-http://10.129.6.142/repos/HDP/HDP-UTILS-1.1.0.21}
AMBARI_REPO_URL=${ambari_repo_url:-http://10.129.6.142/repos/ambari/ambari-2.5.2.0/centos7}
HDP_STACK_VERSION=${hdp_stack_version:-2.6}
HDP_UTILS_VERSION=${hdp_utils_version:-1.1.0.21}
HDP_OS_TYPE=${hdp_os_type:-redhat7}
AMBARI_VERSION=${ambari_version:-2.5.2.0}


#generate and configure ssh key,thereby create the server groups in ansible hosts 
if [ -f ~/.ssh/bootstrap_rsa.pub ]; then
  rm -rf ~/.ssh/bootstrap_rsa*
  > ~/.ssh/known_hosts
fi
ssh-keygen -f ~/.ssh/bootstrap_rsa -t rsa -N ''
echo "generated bootstrap key in ~/.ssh"
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/bootstrap_rsa &>/dev/null
server_count=0
agent_count=0
server_cardinality="1"
agent_cardinality="1"
while read -r foreman_config
do
	host_domain="$(cut -d ' ' -f 1 <<< "${foreman_config}")"
	echo "copying shh key into ${host_domain} domain"
	ssh-keyscan "${host_domain}" >>~/.ssh/known_hosts
	sshpass -p "${HOST_PASSWORD}" ssh-copy-id -i ~/.ssh/bootstrap_rsa.pub "${HOST_USER_NAME}"@"${host_domain}"
	ssh -n "${HOST_USER_NAME}"@"${host_domain}" "rm -rf /etc/yum.repos.d/*"
	scp /etc/yum.repos.d/CentOS-Base.repo "${HOST_USER_NAME}"@"${host_domain}":/etc/yum.repos.d
	scp /etc/yum.repos.d/epel.repo "${HOST_USER_NAME}"@"${host_domain}":/etc/yum.repos.d
	host_domain_temp="$(cut -d '.' -f 1 <<< "${host_domain}")"
	if [[ $host_domain_temp == *"${AMBARI_SERVER_HOST_ID}"* ]]; then
		host_domain_temp="${host_domain_temp}-${AMBARI_SERVER_ID}-${AMBARI_AGENT_ID}"
	elif [[ $host_domain_temp == *"${AMBARI_AGENT_HOST_ID}"* ]];then
        host_domain_temp="${host_domain_temp}-${AMBARI_AGENT_ID}"	
	fi	
    server_group_id_groups="$(cut -d '-' -f 3- <<< "${host_domain_temp}")"
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
done < <(hammer --csv -u "${FOREMAN_USER_NAME}" -p "${FOREMAN_PASSWORD}" host list | grep -vi '^Id' | awk -F, {'print $2'} | grep -vi "^$(hostname -f)" )

#confgure the ansible callback plugin for foreman
echo "configuring the ansible callback plugin for foreman"
FOREMAN_CALLBACK_PLUGIN_DIR="/usr/share/ansible/plugins/callback"
ANSIBLE_CFG="/etc/ansible/ansible.cfg"
FOREMAN_CALLBACK_FILE="foreman_callback.py"
mkdir -p "${FOREMAN_CALLBACK_PLUGIN_DIR}"
sed -i '/callback_plugins/s/^#//g' "${ANSIBLE_CFG}"
sed -i '/bin_ansible_callbacks/s/^#//g' "${ANSIBLE_CFG}"
sed -i '/bin_ansible_callbacks/s/False/True/g' "${ANSIBLE_CFG}"
cp "${FOREMAN_CALLBACK_FILE}" "${FOREMAN_CALLBACK_PLUGIN_DIR}/${FOREMAN_CALLBACK_FILE}"
sed -i "s%<FOREMAN_URL>%https://localhost%g" "${FOREMAN_CALLBACK_PLUGIN_DIR}/${FOREMAN_CALLBACK_FILE}"
sed -i "s%<FOREMAN_SSL_CERT>%/var/lib/puppet/ssl/certs/$(hostname -f).pem%g" "${FOREMAN_CALLBACK_PLUGIN_DIR}/${FOREMAN_CALLBACK_FILE}"
sed -i "s%<FOREMAN_SSL_KEY>%/var/lib/puppet/ssl/private_keys/$(hostname -f).pem%g" "${FOREMAN_CALLBACK_PLUGIN_DIR}/${FOREMAN_CALLBACK_FILE}"
sed -i "s%<FOREMAN_SSL_VERIFY>%0%g" "${FOREMAN_CALLBACK_PLUGIN_DIR}/${FOREMAN_CALLBACK_FILE}"

# execution of playbooks
echo "execution of playbook"
rm -rf executed_playbooks
mkdir executed_playbooks
cp -r  ambari-hdp executed_playbooks/
cd executed_playbooks/ambari-hdp
> inventory/full-dev-platform/hosts
echo -e "${server_groups}" > inventory/full-dev-platform/hosts
GLOBAL_VAR_LOC="inventory/full-dev-platform/group_vars/all"
sed -i "s%<HDP_REPO_URL>%${HDP_REPO_URL}%g" "${GLOBAL_VAR_LOC}"
sed -i "s%<HDP_UTILS_REPO_URL>%${HDP_UTILS_REPO_URL}%g" "${GLOBAL_VAR_LOC}"
sed -i "s%<AMBARI_REPO_URL>%${AMBARI_REPO_URL}%g" "${GLOBAL_VAR_LOC}"
sed -i "s%<AMBARI_VERSION>%${AMBARI_VERSION}%g" "${GLOBAL_VAR_LOC}"
sed -i "s%<HDP_STACK_VERSION>%${HDP_STACK_VERSION}%g" "${GLOBAL_VAR_LOC}"
sed -i "s%<HDP_UTILS_VERSION>%${HDP_UTILS_VERSION}%g" "${GLOBAL_VAR_LOC}"
sed -i "s%<HDP_OS_TYPE>%${HDP_OS_TYPE}%g" "${GLOBAL_VAR_LOC}"
ansible-playbook playbooks/ambari_install.yml

