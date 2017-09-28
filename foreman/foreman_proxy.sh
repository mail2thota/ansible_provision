#setup foreman proxy
#author:Heri Sutrisno
#!/bin/sh
thisdir=`dirname $0`
source ${thisdir}/hammer_cfg.sh

forwarders=$(for i in $(cat /etc/resolv.conf |grep -v '^#'| grep nameserver|awk '{print $2}'); do echo --foreman-proxy-dns-forwarders $i;done) 
#oauth_key=$(grep auth_consumer_key /etc/foreman/settings.yaml | cut -d ' ' -f 2) 
#oauth_secret=$(grep oauth_consumer_secret /etc/foreman/settings.yaml | cut -d ' ' -f 2)
net_interface=$(ip addr | grep "$dhcp_interface:" | cut -d ':' -f 2 | tr -d '[[:space:]]') #check if empty return false
dns_rvs=$(echo $subnet_network | awk 'BEGIN{FS="."}{print $3"."$2"."$1".in-addr.arpa"}')
dns_zone=$(hostname | cut -d '.' -f 2-)
host_ip=$(hostname -i)
host_name=$(hostname)
base_url="https://$host_name"

installSmartProxy(){

    foreman-installer \
        --enable-foreman-plugin-discovery \
        --enable-foreman-proxy-plugin-discovery \
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
        --foreman-proxy-dns=true \
        --foreman-proxy-dns-interface=$net_interface \
        --foreman-proxy-dns-zone=$dns_zone \
        --foreman-proxy-dns-reverse=$dns_rvs \
        ${forwarders} \
        --foreman-proxy-foreman-base-url=$base_url
}

risetPassword(){
    
    password=$(foreman-rake permissions:reset | grep -i "password" | cut -d ':' -f 3 |  tr -d '[[:space:]]')
    echo "export username=\"admin\"" > ${thisdir}/admin.sh
    echo "export password=$password" >> ${thisdir}/admin.sh
}

changeForemanURL(){

    hammer -u $username -p $password settings set --name "unattended_url" --value "http://$(hostname -i)"
    hammer -u $username -p $password settings set --name "foreman_url" --value "https://$(hostname -i)"
}

checkSmartProxy(){
    
    success=$(cat ${thisdir}/log/foreman.log | grep -i -i "Success\!" | wc -l)
    if [ $success -eq 0 ];
    then
        #log:foreman is not installed succesfully
        echo "foreman is not installed succesfully"
        cat ${thisdir}/log/foreman.log
        exit 1
    fi
    cat ${thisdir}/log/foreman.log
}

checkFeatures(){
     
    tftp=$(hammer --csv -u $username -p $password proxy list | /usr/bin/grep -i "$dns_id" | awk '{for(i=1;i<=NF;++i)print $i}'| grep -i "TFTP" | wc -l ) 
    dns=$(hammer --csv -u $username -p $password proxy list | /usr/bin/grep -i "$dns_id" | awk '{for(i=1;i<=NF;++i)print $i}'| grep -i "DNS" | wc -l ) 
    dhcp=$(hammer --csv -u $username -p $password proxy list | /usr/bin/grep -i "$dns_id" | awk '{for(i=1;i<=NF;++i)print $i}'| grep -i "DHCP" | wc -l ) 
    puppet=$(hammer --csv -u $username -p $password proxy list | /usr/bin/grep -i "$dns_id" | awk '{for(i=1;i<=NF;++i)print $i}'| grep -i "Puppet" | wc -l ) 
    ansible=$(hammer --csv -u $username -p $password proxy list | /usr/bin/grep -i "$dns_id" | awk '{for(i=1;i<=NF;++i)print $i}'| grep -i "Ansible" | wc -l ) 
    discovery=$(hammer --csv -u $username -p $password proxy list | /usr/bin/grep -i "$dns_id" | awk '{for(i=1;i<=NF;++i)print $i}'| grep -i "Discovery" | wc -l ) 
     
    if [ $tftp -eq 0 ];
    then
        #log:tftp is not installed properly
        echo "tftp is not installed properly"
        exit 1
    fi

    if [ $dns -eq 0 ];
    then
        #log:dns is not installed properly
        echo "dns is not installed properly"
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

    if [ $discovery -eq 0 ];
    then
        #log:discovery is not installed properly
        echo "discovery is not installed properly"
        exit 1
    fi
}

#risetPassword
installSmartProxy
changeForemanURL
#checkSmartProxy
#checkFeatures

exit 0



