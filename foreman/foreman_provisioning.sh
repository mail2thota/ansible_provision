#!/bin/bash
set -e
thisdir=`dirname $0`
source ${thisdir}/hammer_cfg.sh
source ${thisdir}/logtrace.sh

echo "foreman is ready, start provisioning"
null=0
conn_ready=1
pmaster=$number_of_master
pagent=$number_of_agent
numbers_node=$((pmaster+pagent))
hostgroup_id=$(hammer -u $username -p $password hostgroup list --search \
             "$host_groupname"|/usr/bin/grep -E "(^|\s)$host_groupname($|\s)" \
             |/usr/bin/cut -d' ' -f1)

provisionNodes(){

    until [[ $pmaster -eq $null ]]
    do
       VAR="master$pmaster"
       hammer -u $username -p $password host create --hostgroup-id $hostgroup_id --name "${!VAR}-ambariserver" --mac ${!VAR}  --interface identifier=$dhcp_interface
       check_host=$(hammer -u $username -p $password --csv host list | /usr/bin/grep -i ${!VAR} | awk -F, {'print $5'}| wc -l)
       if [[ $check_host -eq 1 ]];
       then
           pmaster=$((pmaster - 1))
           dcv_ip=$(hammer -u $username -p $password --csv host list | /usr/bin/grep -i ${!VAR} | awk -F, {'print $5'})
           sed -i '1i'"$dcv_ip ${!VAR}"'' $provision_log
           echo "provision node ${!VAR}"
       fi
    done

    until [[ $pagent -eq $null ]]
    do
        VAR="agent$pagent"
        hammer -u $username -p $password host create --hostgroup-id $hostgroup_id --name "${!VAR}-ambariagent" --mac ${!VAR}  --interface identifier=$dhcp_interface
        check_host=$(hammer -u $username -p $password --csv host list | /usr/bin/grep -i ${!VAR} | awk -F, {'print $5'}| wc -l)
        if [[ $check_host -eq 1 ]];
        then
            pagent=$((pagent - 1))
            dcv_ip=$(hammer -u $username -p $password --csv host list | /usr/bin/grep -i ${!VAR} | awk -F, {'print $5'})
            sed -i '1i'"$dcv_ip ${!VAR}"'' $provision_log
            echo "provision node ${!VAR}"
        fi
    done
}

isNodeReady(){

    until [[ $numbers_node -eq $null ]]
    do
    
        ip_file=$(awk 'NR=="'"$numbers_node"'"' $provision_log | awk '{print $1}')
        mac_file=$(awk 'NR=="'"$numbers_node"'"' $provision_log | awk '{print $2}')
        conn_check=`nmap "$ip_file" -p ssh | grep open | grep -i "22/tcp" | wc -l`
        echo "waiting for $mac_file -> $ip_file to be ready"     
        if [[ $conn_check -eq $conn_ready ]];
        then
            echo "$mac_file -> $ip_file is ready"
            numbers_node=$((numbers_node - 1))
        fi 
        sleep 1s
    done
}

provisionNodes
isNodeReady

prov_status="provisioning of nodes has been finished"
echo "$prov_status"
echo "$prov_status" >> $node_log
echo "start the installation of ambari cluster"
sleep 4s

exit 0








