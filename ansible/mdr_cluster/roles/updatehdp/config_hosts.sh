while read host; do
fqdn=$(echo $host | cut -d' ' -f2)
sed -i "/"${fqdn}"/d" /etc/hosts
done < /home/add_hosts

cat /home/add_hosts >> /etc/hosts
