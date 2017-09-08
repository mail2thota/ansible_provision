#!/bin/bash
sudo yum -y install createrepo epel-release firewalld rsync && sudo yum -y install nginx
sudo yum -y update && sudo systemctl reboot



# Create Repository
if [[ $1 == N ]]; then

	#create a "repos" directory to be listed
	sudo mkdir -p /usr/share/nginx/html/repos/centos/7/os/x86_64 	# Base and Update Repos
	sudo mkdir -p /usr/share/nginx/html/repos/centos/7/updates/x86_64
	sudo mkdir -p /usr/share/nginx/html/repos/epel/7/x86_64	# EPEL Repo
	sudo mkdir -p /usr/share/nginx/html/repos/el/7/PC1/x86_64/	#Puppet Labs Repo
	sudo mkdir -p /usr/share/nginx/html/repos/releases/1.15/el7/x86_64/ # Foreman Repo
	sudo mkdir -p /usr/share/nginx/html/repos/plugins/1.15/el7/x86_64/	# Foreman  plugins

	sudo createrepo /usr/share/nginx/html/repos/centos/7/os/x86_64/	# Initialize CentOS Base Repo
	sudo createrepo /usr/share/nginx/html/repos/centos/7/updates/x86_64/	# Initialize CentOS Update Repo
	sudo createrepo /usr/share/nginx/html/repos/epel/7/x86_64/	# Initialize EPEL 7 Repo
	sudo createrepo /usr/share/nginx/html/repos/el/7/PC1/x86_64/	# nitialize Puppet Labs Re[p
	sudo createrepo /usr/share/nginx/html/repos/releases/1.15/el7/x86_64/ # Initialize Foreman 
	sudo createrepo /usr/share/nginx/html/repos/plugins/1.15/el7/x86_64/	# Initialize Foreman  plugins

	#copy all the pre downloaded dependencies from internet to nginx directory
	sudo rsync -avz --exclude='repo*' rsync://mirror.cisp.com/CentOS/7/os/x86_64/ /usr/share/nginx/html/repos/centos/7/os/x86_64/   # CentOS Base Repo
	sudo rsync -avz --exclude='repo*' rsync://mirror.cisp.com/CentOS/7/updates/x86_64/ /usr/share/nginx/html/repos/centos/7/updates/x86_64/   # CentOS Update Repo
	sudo rsync -avz --exclude='repo*' --exclude='debug' rsync://mirrors.rit.edu/epel/7/x86_64/ /usr/share/nginx/html/repos/epel/7/x86_64/   # EPEL 7 Repo
	sudo rsync -avz --exclude='repo*' rsync://yum.puppetlabs.com/el/7/PC1/x86_64/ /usr/share/nginx/html/repos/el/7/PC1/x86_64/ # Puppet Labs repo
	sudo rsync -avz --exclude='repo*' rsync://yum.theforeman.org/releases/1.15/el7/x86_64/ /usr/share/nginx/html/repos/releases/1.15/el7/x86_64/ # Foreman Repo
	sudo rsync -avz --exclude='repo*' rsync://yum.theforeman.org/plugins/1.15/el7/x86_64/ /usr/share/nginx/html/repos/plugins/1.15/el7/x86_64/	# Foreman Plugins

	sudo createrepo --update /usr/share/nginx/html/repos/centos/7/os/x86_64/   # CentOS Base Repo
	sudo createrepo --update /usr/share/nginx/html/repos/centos/7/updates/x86_64/   # CentOS Update Repo
	sudo createrepo --update /usr/share/nginx/html/repos/epel/7/x86_64/   # EPEL 7 Repo
	sudo createrepo --update /usr/share/nginx/html/repos/el/7/PC1/x86_64/ # Puppet Labs repo
	sudo createrepo --update /usr/share/nginx/html/repos/releases/1.15/el7/x86_64/ # Foreman Repo
	sudo createrepo --update /usr/share/nginx/html/repos/plugins/1.15/el7/x86_64/	# Foreman Plugins
else 
	
	if [ ! -d /usr/share/nginx/html/repos/ ]; then
		# copy downloaded folders to nginx repos
		sudo mkdir -p /usr/share/nginx/html/repos/
	fi
	sudo cp /usr/share/repos/ /usr/share/nginx/html/repos/

fi

#provide permissions to nginx
sudo chown :nginx /usr/share/nginx/html/repos/ 

#copy the custom nginx conf to enable repo directory listing & start the nginx service
sudo cp nginx.conf /etc/nginx/
sudo systemctl start nginx

#firewall config
sudo firewall-cmd --permanent --zone=public --add-service=http 
sudo firewall-cmd --permanent --zone=public --add-service=https
sudo firewall-cmd --reload

#enable nginx
sudo systemctl enable nginx

