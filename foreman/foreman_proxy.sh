#!/bin/sh
#author HERI SUTRISNO

REPODIR=`dirname $0`
source ${REPODIR}/hammer_cfg.sh


FORWARDERS=$(for i in $(cat /etc/resolv.conf |grep -v '^#'| grep nameserver|awk '{print $2}'); do echo --foreman-proxy-dns-forwarders $i;done) 

OAUTH_KEY=$(grep auth_consumer_key /etc/foreman/settings.yaml | cut -d ' ' -f 2) 
OAUTH_SECRET=$(grep oauth_consumer_secret /etc/foreman/settings.yaml | cut -d ' ' -f 2)
VIRBR=$(ip addr | grep 'enp0s3:' | cut -d ':' -f 2 | tr -d '[[:space:]]')
DNS_ZONE=$(hostname | cut -d '.' -f 2-)
HOST_IP=$(hostname -i)

echo $FORWARDERS
echo $OAUTH_SECRET
echo $OAUTH_KEY
echo $VIRBR
echo $DNS_ZONE

#foreman-installer --enable-foreman-proxy --foreman-proxy-tftp=true --foreman-proxy-tftp-servername=$HOST_IP --foreman-proxy-dhcp=true --foreman-proxy-dhcp-interface=$VIRBR --foreman-proxy-dhcp-gateway=$SUBNET_GATEWAY --foreman-proxy-dhcp-range="$SUBNET_STARTIP $SUBNET_ENDIP" --foreman-proxy-dhcp-nameservers=$HOST_IP --foreman-proxy-dns=true --foreman-proxy-dns-interface="${VIRBR}" --foreman-proxy-dns-zone="${DNS_ZONE}" --foreman-proxy-dns-reverse=12.11.10.in-addr.arpa ${FORWARDERS} --foreman-proxy-foreman-base-url=https://$hostname --foreman-proxy-oauth-consumer-key="$OAUTH_KEY" --foreman-proxy-oauth-consumer-secret="$OAUTH_SECRET"


HOST_GROUPID=$(hammer -u $USERNAME -p $PASSWORD hostgroup list --search "$HOST_GROUPNAME" | /usr/bin/grep "$HOST_GROUPNAME" | /usr/bin/cut -d' ' -f1)
#NODE1=$(hammer -u $USERNAME -p $PASSWORD discovery list |  /usr/bin/grep "mac080027da0bbb" | /usr/bin/cut -d' ' -f1)
#NODE2=$(hammer $USERNAME -p $PASSWORD discovery list |  /usr/bin/grep "mac0800274ab715" | /usr/bin/cut -d' ' -f1)


until [[ $NODE1 > 0]]
do
   NODE1=$(hammer -u $USERNAME -p $PASSWORD discovery list |  /usr/bin/grep "mac080027da0bbb" | /usr/bin/cut -d' ' -f1)
done

hammer -u $USERNAME -p $PASSWORD discovery provision --id $NODE1 --hostgroup-id $HOST_GROUPID

until [[ $NODE1 > 0]]
do
   NODE2=$(hammer -u $USERNAME -p $PASSWORD discovery list |  /usr/bin/grep "mac080027da0bbb" | /usr/bin/cut -d' ' -f1)
done

#hammer $USERNAME -p $PASSWORD discovery provision --id $NODE2 --hostgroup-id $HOST_GROUPID


#NODE3=$(hammer -u admin -p as123 discovery list |  /usr/bin/grep "mac080027da0bbb" | /usr/bin/cut -d' ' -f1)


NODE1_IP=$(hammer -u $USERNAME -p $PASSWORD discovery info --id $NODE1 |  grep 'IP:' | cut -d ':' -f 2 | tr -d '[[:space:]]') 
#NODE2_IP=$(hammer $USERNAME -p $PASSWORD discovery info --id $NODE2 |  grep 'IP:' | cut -d ':' -f 2 | tr -d '[[:space:]]') 


until [[ $NUMBER_OF_NODES -eq $NULL ]]
do 
    ping -c 1 $NODE1_IP
    STATUS=$?
    if [[ $STATUS -eq $NULL ]]; then
        echo "node ready"
        exit 1
    fi
        echo "waiting node to be ready"       
     sleep 7s
done

#until [[ $NUMBER_OF_NODES -eq $NULL ]]
# do
#   #     ping -c 1 $NODE2_IP       
      #   STATUS=$?
#        if [ $STATUS -ne $NULL ]; then
#            echo "node ready"
#            exit 1
#        fi
         #echo "waiting node to be ready"
#        sleep 5s
  
#    done


echo "proceed to create ambary cluster"


