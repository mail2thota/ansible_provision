#!/bin/bash
sudo yum -y install createrepo epel-release firewalld rsync
sudo yum -y install nginx
sudo yum -y update

# Create Repository
if [[ $1 == N ]]; then
	#create a "repos" directory to be listed
	mkdir -p /usr/share/nginx/html/repos/centos/7/os/x86_64 	# Base and Update Repos
	mkdir -p /usr/share/nginx/html/repos/centos/7/updates/x86_64
	mkdir -p /usr/share/nginx/html/repos/epel/7/x86_64	# EPEL Repo
	mkdir -p /usr/share/nginx/html/repos/el/7/PC1/x86_64/	#Puppet Labs Repo
	mkdir -p /usr/share/nginx/html/repos/releases/1.15/el7/x86_64/ # Foreman Repo
	mkdir -p /usr/share/nginx/html/repos/plugins/1.15/el7/x86_64/	# Foreman  plugins

	createrepo /usr/share/nginx/html/repos/centos/7/os/x86_64/	# Initialize CentOS Base Repo
	createrepo /usr/share/nginx/html/repos/centos/7/updates/x86_64/	# Initialize CentOS Update Repo
	createrepo /usr/share/nginx/html/repos/epel/7/x86_64/	# Initialize EPEL 7 Repo
	createrepo /usr/share/nginx/html/repos/el/7/PC1/x86_64/	# nitialize Puppet Labs Re[p
	createrepo /usr/share/nginx/html/repos/releases/1.15/el7/x86_64/ # Initialize Foreman 
	createrepo /usr/share/nginx/html/repos/plugins/1.15/el7/x86_64/	# Initialize Foreman  plugins

	#copy all the pre downloaded dependencies from internet to nginx directory
	rsync -avz --exclude='repo*' rsync://mirror.cisp.com/CentOS/7/os/x86_64/ /usr/share/nginx/html/repos/centos/7/os/x86_64/   # CentOS Base Repo
	rsync -avz --exclude='repo*' rsync://mirror.cisp.com/CentOS/7/updates/x86_64/ /usr/share/nginx/html/repos/centos/7/updates/x86_64/   # CentOS Update Repo
	rsync -avz --exclude='repo*' --exclude='debug' rsync://mirrors.rit.edu/epel/7/x86_64/ /usr/share/nginx/html/repos/epel/7/x86_64/   # EPEL 7 Repo
	rsync -avz --exclude='repo*' rsync://yum.puppetlabs.com/el/7/PC1/x86_64/ /usr/share/nginx/html/repos/el/7/PC1/x86_64/ # Puppet Labs repo
	rsync -avz --exclude='repo*' rsync://yum.theforeman.org/releases/1.15/el7/x86_64/ /usr/share/nginx/html/repos/releases/1.15/el7/x86_64/ # Foreman Repo
	rsync -avz --exclude='repo*' rsync://yum.theforeman.org/plugins/1.15/el7/x86_64/ /usr/share/nginx/html/repos/plugins/1.15/el7/x86_64/	# Foreman Plugins

	createrepo --update /usr/share/nginx/html/repos/centos/7/os/x86_64/   # CentOS Base Repo
	createrepo --update /usr/share/nginx/html/repos/centos/7/updates/x86_64/   # CentOS Update Repo
	createrepo --update /usr/share/nginx/html/repos/epel/7/x86_64/   # EPEL 7 Repo
	createrepo --update /usr/share/nginx/html/repos/el/7/PC1/x86_64/ # Puppet Labs repo
	createrepo --update /usr/share/nginx/html/repos/releases/1.15/el7/x86_64/ # Foreman Repo
	createrepo --update /usr/share/nginx/html/repos/plugins/1.15/el7/x86_64/	# Foreman Plugins

elif [ ! -d /usr/share/nginx/html/repos/ ]; then
	# copy downloaded folders to nginx repos
	mkdir -p /usr/share/nginx/html/repos/
	cp /usr/share/repos/ /usr/share/nginx/html/repos/
fi

#provide permissions to nginx
sudo chown :nginx /usr/share/nginx/html/repos/ 

#copy the custom nginx conf to enable repo directory listing & start the nginx service
cp nginx.conf /etc/nginx/
systemctl start nginx

#firewall config
firewall-cmd --permanent --zone=public --add-service=http 
firewall-cmd --permanent --zone=public --add-service=https
firewall-cmd --reload

#enable nginx
systemctl enable nginx