#!/bin/bash
hosts_file=$(awk '$1=$1' ORS='\\n' /etc/hosts)
if [[ $hosts_file == *"#cluster nodes start"* ]];then
sed -i '/start/,/end/d' /etc/hosts
fi
echo "#cluster nodes start" >>/etc/hosts
cat /home/all_config/host_list  >> /etc/hosts
echo "#cluster nodes end" >> /etc/hosts