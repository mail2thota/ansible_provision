#provisioning of foreman
#author:Heri Sutrisno
#!/bin/bash

thisdir=`dirname $0`
source ${thisdir}/hammer_cfg.sh

echo "foreman is ready, start provisioning"

null=0
conn_ready=1
pb=$numbers_of_node
px=$numbers_of_node
provision_log="${thisdir}/log/list_node.log"
log_dir="${thisdir}/log"

setLogFile(){

    node_log="${thisdir}/log/foreman.log"
    if [ ! -d "$log_dir" ]; 
    then
        mkdir -p $log_dir 
    fi

    if [ ! -e $node_log ]; 
    then
        echo "create $node_log"
        echo > $node_log
    fi

    if [ ! -e $provision_log ]; 
    then
        echo "create $provision_log"
        echo > $provision_log
        return 1
    fi

    echo "" > $provision_log
    echo "" > $node_log
}



pmaster=$number_of_master
pagent=$number_of_agent
numbers_node=$((pmaster+pagent))
hostgroup_id=$(hammer -u $username -p $password hostgroup list --search "$host_groupname" | /usr/bin/grep -E "(^|\s)$host_groupname($|\s)" | /usr/bin/cut -d' ' -f1)

provisionNodes(){

until [[ $pmaster -eq $null ]]
do
   VAR="master$pmaster"
   hammer -u $username -p $password host create --hostgroup-id $hostgroup_id --name "${!VAR}-ambariservers" --mac ${!VAR}  --interface identifier=$dhcp_interface
   check_host=$(hammer -u $username -p $password --csv host list | /usr/bin/grep ${!VAR} | awk -F, {'print $5'}| wc -l)
   if [[ $check_host -eq 1 ]];
   then
       pmaster=$((pmaster - 1))
       dcv_ip=$(hammer -u $username -p $password --csv host list | /usr/bin/grep ${!VAR} | awk -F, {'print $5'})
       sed -i '1i'"$dcv_ip ${!VAR}"'' $provision_log
       echo "provision node ${!VAR}"
   fi
done

until [[ $pagent -eq $null ]]
do
    VAR="agent$pagent"
    hammer -u $username -p $password host create --hostgroup-id $hostgroup_id --name "${!VAR}-ambariagent" --mac ${!VAR}  --interface identifier=$dhcp_interface
    check_host=$(hammer -u $username -p $password --csv host list | /usr/bin/grep ${!VAR} | awk -F, {'print $5'}| wc -l)
    if [[ $check_host -eq 1 ]];
    then
        pagent=$((pagent - 1))
        dcv_ip=$(hammer -u $username -p $password --csv host list | /usr/bin/grep ${!VAR} | awk -F, {'print $5'})
        sed -i '1i'"$dcv_ip ${!VAR}"'' $provision_log
        echo "provision node ${!VAR}"
    fi
done
}

discoveryNodes(){
   
    host_groupid=$(hammer --csv -u $username -p $password hostgroup list | /usr/bin/grep -i "$host_groupname" | awk -F, '{print $1}')
    until [[ $px -eq $null ]]
    do
        dcv_nodes=$(hammer --csv -u $username -p $password discovery list | grep -vi '^ID' | awk -F, {'print $2'} | wc -l)
        remaining_nodes=$((numbers_of_node - dcv_nodes))
        echo "numbers of node's been discovered: $dcv_nodes"
        echo "waiting $remaining_nodes remaining of nodes to be discovered from total $numbers_of_node nodes"

        if [ $dcv_nodes -eq $numbers_of_node ];
        then
            echo "total $numbers_of_node has been discovered, provisioning will be begin"
            until [[ $px -eq $null ]]
            do
                macaddr=$(hammer --csv -u $username -p $password discovery list | grep -vi '^ID' | awk -F, 'NR=="'"$px"'"{print $2}')
                nodeid=$(hammer --csv -u $username -p $password discovery list | /usr/bin/grep -i "$macaddr" | awk -F, '{print $1}')
                dcv_ip=$(hammer -u $username -p $password discovery info --id $nodeid | /usr/bin/grep -i "IP" | awk '{print $2}')
                sed -i '1i'"$dcv_ip $macaddr"'' $provision_log
                echo "provision node $macaddr"
                rm -rf /var/lib/dhcpd/dhcpd.leases~
                echo "" > /var/lib/dhcpd/dhcpd.leases
                systemctl restart dhcpd
                hammer -u $username -p $password discovery provision --id $nodeid --hostgroup-id $host_groupid
            
                px=$((px - 1))
           done
        fi
        sleep 1s
    done
}

isNodeReady(){

    until [[ $numbers_node -eq $null ]]
    do
    
        ip_file=$(awk 'NR=="'"$numbers_node"'"' $provision_log | awk '{print $1}')
        mac_file=$(awk 'NR=="'"$numbers_node"'"' $provision_log | awk '{print $2}')
        conn_check=`nmap "$ip_file" -p ssh | grep open | grep -i "22/tcp" | wc -l`
        echo "waiting for $mac_file -> $ip_file to be ready"     
        #conn_check=1
        if [[ $conn_check -eq $conn_ready ]];
        then
            echo "$mac_file -> $ip_file is ready"
            numbers_node=$((numbers_node - 1))
        fi 
        sleep 1s
    done
}

setLogFile
provisionNodes
#discoveryNodes
isNodeReady

prov_status="provisioning of nodes has been finished"
echo "$prov_status"
echo "$prov_status" >> ${thisdir}/log/foreman.log
echo "start the installation of ambari cluster"
sleep 4s

exit 0








