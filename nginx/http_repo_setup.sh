#!/bin/bash
yum install -y epel-release
yum install -y nginx

#create a static "repo" directory to be listed
mkdir -p /usr/share/nginx/html/repo/

#copy all the pre downloaded dependencies from /usr/share/repo/ to nginx  
cp /usr/share/repo/ /usr/share/nginx/html/repo/

#provide permissions to nginx
chown :nginx /usr/share/nginx/html/repo/ 

#copy the custom nginx conf to enable repo directory listing & start the nginx service
systemctl start nginx

#firewall config
firewall-cmd --permanent --zone=public --add-service=http 
firewall-cmd --permanent --zone=public --add-service=https
firewall-cmd --reload

#enable nginx
systemctl enable nginx

