#!/bin/bash
#install and manage dns
#author:Heri Sutrisno
#email:herygranding@gmail.com
set -e
thisdir=`dirname $0`
source  ${thisdir}/../hammer_cfg.sh

filep="${thisdir}/hostlist"
sed -i "s/ //g" $filep
sed -i '/^$/d' $filep
number_hosts=$(wc -l < $filep)
null=0
masterip=$(ip addr show enp0s3 | grep -Po 'inet \K[\d.]+')
masterhost=`hostname|cut -d"." -f1`

yum -y install bind bind-utils
systemctl enable named
systemctl stop named

createBind(){

    echo ";A record hostname to ip address" >>  /var/named/db.${domain}
    until [[ $number_hosts -eq $null ]]
    do

        hostname=$(awk 'NR=="'"$number_hosts"'"' $filep | awk -F"=" '{print $1}')
        ip_file=$(awk 'NR=="'"$number_hosts"'"' $filep | awk -F"=" '{print $2}')
        echo "www     IN     A     ${ip_file} 
${hostname}     IN     A     ${ip_file}" >> /var/named/db.${domain}
        echo "${number_hosts}     IN     PTR     ${hostname}.${domain}." >> /var/named/12.11.10.db
         
            number_hosts=$((number_hosts - 1))
        sleep 1s
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
