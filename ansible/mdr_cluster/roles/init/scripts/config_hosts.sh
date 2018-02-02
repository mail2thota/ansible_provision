while read host; do
fqdn=$(echo $host | cut -d' ' -f2)
sed -i "/"${fqdn}"/d" /etc/hosts
done < /home/$1/host_list

cat /home/$1/host_list >> /etc/hosts
