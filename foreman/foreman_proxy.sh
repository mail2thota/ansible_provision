#!/bin/sh
set -e
thisdir=`dirname $0`
source ${thisdir}/hammer_cfg.sh
source ${thisdir}/logtrace.sh

#check if empty return false
net_interface=$(ip addr | grep "$dhcp_interface:" | cut -d ':' -f 2 | tr -d '[[:space:]]')
host_ip=$(hostname -i)
host_name=$(hostname)
base_url="https://$host_name"

installSmartProxy(){

    foreman-installer \
        --foreman-configure-epel-repo=false \
        --foreman-configure-scl-repo=false \
        --enable-foreman-plugin-ansible \
        --enable-foreman-proxy-plugin-ansible \
        --foreman-admin-username=$username \
        --foreman-admin-password=$password \
        --enable-foreman-proxy \
        --foreman-proxy-tftp=true \
        --foreman-proxy-tftp-servername=$host_ip \
        --foreman-proxy-dhcp=true \
        --foreman-proxy-dhcp-interface=$net_interface \
        --foreman-proxy-dhcp-gateway=$subnet_gateway \
        --foreman-proxy-dhcp-range="$subnetip_start $subnetip_end" \
        --foreman-proxy-dhcp-nameservers=$host_ip \
        --foreman-proxy-dns=false \
        --foreman-proxy-dns-managed=false \
        --foreman-proxy-foreman-base-url=$base_url > $node_log
}

changeForemanURL(){

    hammer -u $username -p $password settings set --name "unattended_url" --value "http://$(hostname -i)"
    hammer -u $username -p $password settings set --name "foreman_url" --value "https://$(hostname -i)"
}

checkSmartProxy(){
    
    success=$(cat $node_log | grep -i -i "Success\!" | wc -l)
    if [ $success -eq 0 ];
    then
        #log:foreman is not installed succesfully
        echo "foreman is not installed succesfully"
        cat $node_log
        exit 1
    fi
    cat $node_log
}

checkFeatures(){
     
    tftp=$(hammer --csv -u $username -p $password proxy list | /usr/bin/grep -i "$dns_id" | awk '{for(i=1;i<=NF;++i)print $i}'| grep -i "TFTP" | wc -l ) 
    dhcp=$(hammer --csv -u $username -p $password proxy list | /usr/bin/grep -i "$dns_id" | awk '{for(i=1;i<=NF;++i)print $i}'| grep -i "DHCP" | wc -l ) 
    puppet=$(hammer --csv -u $username -p $password proxy list | /usr/bin/grep -i "$dns_id" | awk '{for(i=1;i<=NF;++i)print $i}'| grep -i "Puppet" | wc -l ) 
    ansible=$(hammer --csv -u $username -p $password proxy list | /usr/bin/grep -i "$dns_id" | awk '{for(i=1;i<=NF;++i)print $i}'| grep -i "Ansible" | wc -l ) 
     
    if [ $tftp -eq 0 ];
    then
        #log:tftp is not installed properly
        echo "tftp is not installed properly"
        exit 1
    fi
    
    if [ $dhcp -eq 0 ];
    then
        #log:dhcp is not installed properly
        echo "dhcp is not installed properly"
        exit 1
    fi

    if [ $puppet -eq 0 ];
    then
        #log:puppet is not installed properly
        echo "puppet $puppet"
        echo "puppet is not installed properly"
        exit 1
    fi

    if [ $ansible -eq 0 ];
    then
        #log:ansible is not installed properly
        echo "ansible is not installed properly"
        exit 1
    fi

    echo "DHCP,TFTP,ANSIBLE,PUPPET are installed"
}

setLogFile
installSmartProxy
changeForemanURL
checkSmartProxy
checkFeatures

exit 0



