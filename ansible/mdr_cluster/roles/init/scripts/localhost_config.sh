#!/bin/bash
hosts_file=$(awk '$1=$1' ORS='\\n' /etc/hosts)
if [[ $hosts_file == *"#mdr_hosts_begins"* ]];then
sed -i '/mdr_hosts_begins/,/mdr_hosts_ends/d' /etc/hosts
fi
echo "#mdr_hosts_begins" >>/etc/hosts
cat /home/$1/host_list  >> /etc/hosts
echo "#mdr_hosts_ends" >> /etc/hosts
