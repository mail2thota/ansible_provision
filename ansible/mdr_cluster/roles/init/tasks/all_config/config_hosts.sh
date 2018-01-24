while read host; do
fqdn=$(echo $host | cut -d' ' -f2)
sed -i "/"${fqdn}"/d" /etc/hosts
done < /home/all_config/host_list

cat /home/all_config/host_list >> /etc/hosts
