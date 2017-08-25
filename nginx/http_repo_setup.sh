#!/bin/bash
yum install -y epel-release
yum install -y nginx
mkdir -p /usr/share/nginx/html/repo/
#This must be changed to real repo config or downloads
touch index.html
cp index.html /usr/share/nginx/html/repo/
chown :nginx /usr/share/nginx/html/repo/ 

systemctl start nginx
firewall-cmd --permanent --zone=public --add-service=http 
firewall-cmd --permanent --zone=public --add-service=https
firewall-cmd --reload
cp nginx.conf /etc/nginx/
systemctl enable nginx

