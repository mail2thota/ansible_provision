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
	mkdir -p /usr/share/nginx/html/repos/puppet/el/7/PC1/x86_64/	#Puppet Labs Repo
	mkdir -p /usr/share/nginx/html/repos/foreman/1.15/el7/x86_64/ # Foreman Repo
	mkdir -p /usr/share/nginx/html/repos/foreman_plugin/1.15/el7/x86_64/	# Foreman  plugins
	mkdir -p /usr/share/nginx/html/repos/centos/7/sclo/x86_64/rh/ #rh
	mkdir -p /usr/share/nginx/html/repos/centos/7/sclo/x86_64/sclo/ #sclo
	mkdir -p /usr/share/nginx/html/repos/pki/x86_64/ #pki
	
	createrepo /usr/share/nginx/html/repos/centos/7/os/x86_64/	# Initialize CentOS Base Repo
	createrepo /usr/share/nginx/html/repos/centos/7/updates/x86_64/	# Initialize CentOS Update Repo
	createrepo /usr/share/nginx/html/repos/epel/7/x86_64/	# Initialize EPEL 7 Repo
	createrepo /usr/share/nginx/html/repos/puppet/el/7/PC1/x86_64/	# nitialize Puppet Labs Re[p
	createrepo /usr/share/nginx/html/repos/foreman/1.15/el7/x86_64/ # Initialize Foreman 
	createrepo /usr/share/nginx/html/repos/foreman_plugin/1.15/el7/x86_64/	# Initialize Foreman  plugins
	createrepo /usr/share/nginx/html/repos/centos/7/sclo/x86_64/rh/ #Initialize rh
	createrepo /usr/share/nginx/html/repos/centos/7/sclo/x86_64/sclo/ #Initialize sclo
	
	#copy all the pre downloaded dependencies from internet to nginx directory
	rsync -avz --exclude='repo*' rsync://mirror.cisp.com/CentOS/7/os/x86_64/ /usr/share/nginx/html/repos/centos/7/os/x86_64/   # CentOS Base Repo
	rsync -avz --exclude='repo*' rsync://mirror.cisp.com/CentOS/7/updates/x86_64/ /usr/share/nginx/html/repos/centos/7/updates/x86_64/   # CentOS Update Repo
	rsync -avz --exclude='repo*' --exclude='debug' rsync://mirrors.rit.edu/epel/7/x86_64/ /usr/share/nginx/html/repos/epel/7/x86_64/   # EPEL 7 Repo
	rsync -avz --exclude='repo*' rsync://yum.puppetlabs.com/el/7/PC1/x86_64/ /usr/share/nginx/html/repos/puppet/el/7/PC1/x86_64/ # Puppet Labs repo
	rsync -avz --exclude='repo*' rsync://yum.theforeman.org/releases/1.15/el7/x86_64/ /usr/share/nginx/html/repos/foreman/1.15/el7/x86_64/ # Foreman Repo
	rsync -avz --exclude='repo*' rsync://yum.theforeman.org/plugins/1.15/el7/x86_64/ /usr/share/nginx/html/repos/foreman_plugin/1.15/el7/x86_64/	# Foreman Plugins
	rsync -avz --exclude='repo*' rsync://mirror.cisp.com/CentOS/7/sclo/x86_64/rh /usr/share/nginx/html/repos/centos/7/sclo/x86_64/rh/ #rh
	rsync -avz --exclude='repo*' rsync://mirror.cisp.com/CentOS/7/sclo/x86_64/sclo /usr/share/nginx/html/repos/centos/7/sclo/x86_64/sclo/ #sclo
	
	
	createrepo --update /usr/share/nginx/html/repos/centos/7/os/x86_64/   # CentOS Base Repo
	createrepo --update /usr/share/nginx/html/repos/centos/7/updates/x86_64/   # CentOS Update Repo
	createrepo --update /usr/share/nginx/html/repos/epel/7/x86_64/   # EPEL 7 Repo
	createrepo --update /usr/share/nginx/html/repos/puppet/el/7/PC1/x86_64/ # Puppet Labs repo
	createrepo --update /usr/share/nginx/html/repos/foreman/1.15/el7/x86_64/ # Foreman Repo
	createrepo --update /usr/share/nginx/html/repos/foreman_plugin/1.15/el7/x86_64/	# Foreman Plugins
	createrepo --update /usr/share/nginx/html/repos/centos/7/sclo/x86_64/rh/ #rh
	createrepo --update /usr/share/nginx/html/repos/centos/7/sclo/x86_64/sclo/ #sclo
	
	#Download all GPG keys
	wget http://mirror.cisp.com/CentOS/7/os/x86_64/RPM-GPG-KEY-CentOS-7
	sudo mv RPM-GPG-KEY-CentOS-7 /usr/share/nginx/html/repos/pki/x86_64/
	wget https://yum.stanford.edu/RPM-GPG-KEY-CentOS-SIG-SCLo
	sudo mv RPM-GPG-KEY-CentOS-SIG-SCLo /usr/share/nginx/html/repos/pki/x86_64/
	wget http://mirrors.rit.edu/epel/RPM-GPG-KEY-EPEL-7
	sudo mv RPM-GPG-KEY-EPEL-7 /usr/share/nginx/html/repos/pki/x86_64/
	wget http://yum.theforeman.org/releases/1.15/RPM-GPG-KEY-foreman
	sudo mv RPM-GPG-KEY-foreman /usr/share/nginx/html/repos/pki/x86_64/
	wget https://yum.puppetlabs.com/RPM-GPG-KEY-puppet
	sudo mv RPM-GPG-KEY-puppet /usr/share/nginx/html/repos/pki/x86_64/
	wget https://yum.puppetlabs.com/RPM-GPG-KEY-puppetlabs
	sudo mv RPM-GPG-KEY-puppetlabs /usr/share/nginx/html/repos/pki/x86_64/
	
	
	#Download CentOS ISO image
	wget http://archive.kernel.org/centos-vault/7.1.1503/isos/x86_64/CentOS-7-x86_64-Everything-1503-01.iso
	sudo mv CentOS-* /usr/share/nginx/html/repos/
	
	#Download ambari
	http://public-repo-1.hortonworks.com/ambari/centos6/2.x/updates/2.5.0.3/ambari-2.5.0.3-centos6.tar.gz
	sudo mv ambari-2.5.0.3-centos6.tar.gz /usr/share/nginx/html/repos/
	tar -xvf /usr/share/nginx/html/repos/ambari-2.5.0.3-centos6.tar.gz
	
	#Download HDP
	wget http://public-repo-1.hortonworks.com/HDP/centos7/2.x/updates/2.6.2.0/HDP-2.6.2.0-centos7-rpm.tar.gz
	sudo mv HDP-2.6.2.0-centos7-rpm.tar.gz /usr/share/nginx/html/repos/
	tar -xvf /usr/share/nginx/html/repos/HDP-2.6.2.0-centos7-rpm.tar.gz
	

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