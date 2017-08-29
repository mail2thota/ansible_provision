#!/bin/bash
yum -y install createrepo epel-release firewalld rsync && yum -y install nginx
yum -y update && systemctl reboot

#create a static "repo" directory to be listed
mkdir -p /usr/share/nginx/html/repos/centos/7/os/x86_64 	# Base and Update Repos
mkdir -p /usr/share/nginx/html/repos/centos/7/updates/x86_64
mkdir -p /usr/share/nginx/html/repos/epel/7/x86_64	# EPEL Repo

createrepo /usr/share/nginx/html/repos/centos/7/os/x86_64/	# Initialize CentOS Base Repo
createrepo /usr/share/nginx/html/repos/centos/7/updates/x86_64/	# Initialize CentOS Update Repo
createrepo /usr/share/nginx/html/repos/epel/7/x86_64/	# Initialize EPEL 7 Repo

#copy all the pre downloaded dependencies from internet to nginx directory
rsync -avz --exclude='repo*' rsync://mirror.cisp.com/CentOS/7/os/x86_64/ /usr/share/nginx/html/repos/centos/7/os/x86_64/   # CentOS Base Repo
rsync -avz --exclude='repo*' rsync://mirror.cisp.com/CentOS/7/updates/x86_64/ /usr/share/nginx/html/repos/centos/7/updates/x86_64/   # CentOS Update Repo
rsync -avz --exclude='repo*' --exclude='debug' rsync://mirrors.rit.edu/epel/7/x86_64/ /usr/share/nginx/html/repos/epel/7/x86_64/   # EPEL 7 Repo

createrepo --update /usr/share/nginx/html/repos/centos/7/os/x86_64/   # CentOS Base Repo
createrepo --update /usr/share/nginx/html/repos/centos/7/updates/x86_64/   # CentOS Update Repo
createrepo --update /usr/share/nginx/html/repos/epel/7/x86_64/   # EPEL 7 Repo

#provide permissions to nginx
chown :nginx /usr/share/nginx/html/repos/ 

#copy the custom nginx conf to enable repo directory listing & start the nginx service
systemctl start nginx

#firewall config
firewall-cmd --permanent --zone=public --add-service=http 
firewall-cmd --permanent --zone=public --add-service=https
firewall-cmd --reload

#enable nginx
systemctl enable nginx

