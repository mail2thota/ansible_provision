#!/bin/bash
#install and manage dns
#author:Heri Sutrisno
#email:herygranding@gmail.com
set -e
thisdir=`dirname $0`
source  ${thisdir}/../hammer_cfg.sh

null=0
masterip=$(ip addr show enp0s3 | grep -Po 'inet \K[\d.]+')
masterhost=`hostname|cut -d"." -f1`

yum -y install bind bind-utils
systemctl enable named
systemctl stop named

pmaster=$number_of_master
pagent=$number_of_agent
numbers_node=$((pmaster+pagent))

createBind(){

    echo ";A record hostname to ip address" >>  /var/named/db.${domain}
    until [[ $pmaster -eq $null ]]
    do
       VAR="master$pmaster"
       VARIP="${VAR}ip"
       echo "www     IN     A     ${!VARIP} 
${VAR}-ambariserver     IN     A     ${!VARIP}" >> /var/named/db.${domain}
       echo "${numbers_node}     IN     PTR     ${VAR}-ambariserver.${domain}." >> /var/named/12.11.10.db
       pmaster=$((pmaster - 1))
       numbers_node=$((numbers_node-1))  
    done

    until [[ $pagent -eq $null ]]
    do
        VAR="agent$pagent"
        VARIP="${VAR}ip"
        echo "www     IN     A     ${!VARIP} 
${VAR}-ambariagent     IN     A     ${!VARIP}" >> /var/named/db.${domain}
       echo "${numbers_node}     IN     PTR     ${VAR}-ambariagent.${domain}." >> /var/named/12.11.10.db      
       pagent=$((pagent - 1))
       numbers_node=$((numbers_node-1))
    done
}

setZone(){
echo "
\$TTL 604800
@ IN SOA ${masterhost}.${domain}.  root.${domain}.  (
  5           ;serial
  604800      ;Refresh
  86400       ;Retry
  2419200     ;Expire
  604800      ;Minimum TTL
)
;Name Server Information
@    IN   NS     ${masterhost}.${domain}.

; A records for name servers
${masterhost}       IN   A      ${masterip}" >  /var/named/db.${domain}

echo "
\$TTL 604800
@ IN SOA ${masterhost}.${domain}.  root.${domain}.  (
  5           ;serial
  604800      ;Refresh
  86400       ;Retry
  2419200     ;Expire
  604800      ;Minimum TTL
)
;Name Server Information
@    IN   NS     ${masterhost}.${domain}.

;reverse lookup for name server
1     IN     PTR     ${masterhost}.${domain}.


; ptr record
       IN   PTR   www.${domain}." > /var/named/12.11.10.db
}
setZone
createBind

cp -f ${thisdir}/named.conf /etc
chmod 755 /var/named/db.${domain}
chmod 755 /var/named/12.11.10.db
chmod 755 /etc/named.conf
systemctl start named

exit 0
