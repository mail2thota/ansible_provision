#!/bin/bash

thisdir=`dirname $0`
source ${thisdir}/../foreman/hammer_cfg.sh

set -e

HOST_USER_NAME=${node_user:-root}
HOST_PASSWORD=${node_pass:-as12345678}
FOREMAN_USER_NAME=${username:-admin}
FOREMAN_PASSWORD=${password:-as123}

#generate and configure ssh key,thereby create the server groups in ansible hosts
if [ -f ~/.ssh/bootstrap_rsa.pub ]; then
  rm -rf ~/.ssh/bootstrap_rsa*
  > ~/.ssh/known_hosts
fi
ssh-keygen -f ~/.ssh/bootstrap_rsa -t rsa -N ''
echo "generated bootstrap key in ~/.ssh"
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/bootstrap_rsa &>/dev/null
server_count=1
agent_count=7

server_cardinality="1"
agent_cardinality="7"
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

# execution of playbooks
echo "execution of playbook"
rm -rf executed_playbooks
mkdir executed_playbooks
cp -r  ambari-hdp executed_playbooks/

cd executed_playbooks/ambari-hdp
ansible-playbook playbooks/pre-config.yml
ansible-playbook playbooks/ambari_install.yml 

