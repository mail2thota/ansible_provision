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

    until [[ $pb -eq $null ]]
    do
    
        ip_file=$(awk 'NR=="'"$pb"'"' $provision_log | awk '{print $1}')
        mac_file=$(awk 'NR=="'"$pb"'"' $provision_log | awk '{print $2}')
        conn_check=`nmap "$ip_file" -p ssh | grep open | grep -i "22/tcp" | wc -l`
        echo "waiting for $mac_file -> $ip_file to be ready"     
        #conn_check=1
        if [[ $conn_check -eq $conn_ready ]];
        then
            echo "$mac_file -> $ip_file is ready"
            pb=$((pb - 1))
        fi 
        sleep 1s
    done
}

setLogFile
discoveryNodes
isNodeReady

prov_status="provisioning of $numbers_of_node nodes has been finished"
echo "$prov_status"
echo "$prov_status" >> ${thisdir}/log/foreman.log
echo "start the installation of ambari cluster"
sleep 4s

exit 0








