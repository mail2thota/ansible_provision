#!/bin/bash
#install and manage dns
#author:Heri Sutrisno
#email:herygranding@gmail.com
set -e
thisdir=`dirname $0`
source  ${thisdir}/hammer_cfg.sh

null=0
masterip=$(ip addr show enp0s3 | grep -Po 'inet \K[\d.]+')
last_ip=`echo $masterip | cut -d . -f 4`
masterhost=`hostname|cut -d"." -f1`
dns_rvs=$(echo $subnet_network | awk 'BEGIN{FS="."}{print $3"."$2"."$1".in-addr.arpa"}')

yum -y install bind bind-utils
systemctl enable named
systemctl stop named

pmaster=$number_of_master
pagent=$number_of_agent

createBind(){

    echo "; ${subnet_network} - A records" >>  /var/named/forward.${domain}
    until [[ $pmaster -eq $null ]]
    do
       VAR="master$pmaster"
       VARIP="${VAR}ip"
       echo "${VAR}-ambariserver   IN     A     ${!VARIP}" >> /var/named/forward.${domain}
       last_ip=`echo ${!VARIP} | cut -d . -f 4`
       echo "$last_ip     IN     PTR     ${VAR}-ambariserver.${domain}." >> /var/named/reverse.${domain}
       pmaster=$((pmaster - 1))
    done

    until [[ $pagent -eq $null ]]
    do
       VAR="agent$pagent"
       VARIP="${VAR}ip"
       echo "${VAR}-ambariagent     IN     A     ${!VARIP}" >> /var/named/forward.${domain}
       last_ip=`echo ${!VARIP} | cut -d . -f 4`
       echo "$last_ip     IN     PTR     ${VAR}-ambariagent.${domain}." >> /var/named/reverse.${domain}
       pagent=$((pagent - 1))
    done
}

setZone(){
echo "\$TTL 604800
@ IN SOA ${masterhost}.${domain}.  root.${domain}.  (
  2017101001  ;serial
  604800      ;Refresh
  86400       ;Retry
  2419200     ;Expire
  604800      ;Minimum TTL
)
; name servers - NS records
@    IN   NS     ${masterhost}.${domain}.

; name servers - A records
${masterhost}    IN   A      ${masterip}" >  /var/named/forward.${domain}

echo "\$TTL 604800
@ IN SOA ${masterhost}.${domain}.  root.${domain}.  (
  2017101001  ;serial
  604800      ;Refresh
  86400       ;Retry
  2419200     ;Expire
  604800      ;Minimum TTL
)
; name servers - NS records
@      IN     NS      ${masterhost}.${domain}.

; reverse lookup for name server
${last_ip}      IN     PTR     ${masterhost}.${domain}.
; PTR records IP address to hostname" > /var/named/reverse.${domain}
}

setNamedConf(){

echo "
options {
        listen-on port 53 { 127.0.0.1;${masterip}; };
        directory       \"/var/named\";
        dump-file       \"/var/named/data/cache_dump.db\";
        statistics-file \"/var/named/data/named_stats.txt\";
        memstatistics-file \"/var/named/data/named_mem_stats.txt\";
        allow-query     { localhost;${subnet_network}/24; };
        recursion yes;
        dnssec-enable yes;
        dnssec-validation yes;
        dnssec-lookaside auto;

        bindkeys-file \"/etc/named.iscdlv.key\";
        managed-keys-directory \"/var/named/dynamic\";
        pid-file \"/run/named/named.pid\";
        session-keyfile \"/run/named/session.key\";
};

logging {
        channel default_debug {
                file \"data/named.run\";
                severity dynamic;
        };
};

zone \".\" IN {
type hint;
file \"named.ca\";
};


zone \"${domain}\" IN {
type master;
file \"forward.${domain}\";
allow-update { none; };
};

zone \"${dns_rvs}\" IN {
type master;
file \"reverse.${domain}\";
allow-update { none; };
};

include \"/etc/named.rfc1912.zones\";
include \"/etc/named.root.key\";" > /etc/named.conf
}

setNamedConf
setZone
createBind

chmod 755 /var/named/forward.${domain}
chmod 755 /var/named/reverse.${domain}
chmod 755 /etc/named.conf
systemctl start named

exit 0
