#!/bin/sh

#author:Heri Sutrisno




#--foreman-plugin-discovery-install-images=true

# Update system first

1.install nmap
yum install -y nmap nmap-ncat
2.check status
nmap=/usr/bin/nmap --version | grep "6.40" | wc -l
if [ $nmap -ne 1 ]
then
stop installation
fi
3.create log dir:mkdir ${REPODIR}/log

if puppet agent --version | grep "3." | grep -v grep 2> /dev/null
then
    echo "Puppet Agent $(puppet agent --version) is already installed. Moving on..."
else
    echo "Puppet Agent $(puppet agent --version) installed. Replacing..."

    sudo rpm -ivh http://yum.puppetlabs.com/puppetlabs-release-pc1-el-7.noarch.rpm && \
    sudo yum -y erase puppet-agent && \
    sudo rm -f /etc/yum.repos.d/puppetlabs-pc1.repo && \
    sudo yum clean all
fi

if ps aux | grep "/usr/share/foreman" | grep -v grep 2> /dev/null
then
    echo "Foreman appears to all already be installed. Exiting..."
else
    sudo yum -y install epel-release http://yum.theforeman.org/releases/1.15/el7/x86_64/foreman-release.rpm && \
    sudo yum -y install foreman-installer nano nmap-ncat && \
    sudo foreman-installer --enable-foreman-plugin-discovery --enable-foreman-proxy-plugin-discovery --enable-foreman-plugin-ansible --enable-foreman-proxy-plugin-ansible 
    yum install tfm-rubygem-hammer_cli_foreman_discovery
    # Set-up firewall
    # https://www.digitalocean.com/community/tutorials/additional-recommended-steps-for-new-centos-7-servers
    #sudo firewall-cmd --permanent --add-service=http
    #sudo firewall-cmd --permanent --add-service=https
    #sudo firewall-cmd --permanent --add-port=69/tcp
    #sudo firewall-cmd --permanent --add-port=67-69/udp
    #sudo firewall-cmd --permanent --add-port=53/tcp
    #sudo firewall-cmd --permanent --add-port=53/udp
    #sudo firewall-cmd --permanent --add-port=8443/tcp
    #sudo firewall-cmd --permanent --add-port=8140/tcp

    #sudo firewall-cmd --reload
    #sudo systemctl enable firewalld

    # First run the Puppet agent on the Foreman host which will send the first Puppet report to Foreman,
    # automatically creating the host in Foreman's database
    sudo puppet agent --test --waitforcert=60

    # Optional, install some optional puppet modules on Foreman server to get started...
   # sudo puppet module install -i /etc/puppet/environments/production/modules puppetlabs-ntp
    #sudo puppet module install -i /etc/puppet/environments/production/modules puppetlabs-git
    #sudo puppet module install -i /etc/puppet/environments/production/modules puppetlabs-vcsrepo
    #sudo puppet module install -i /etc/puppet/environments/production/modules garethr-docker
    #sudo puppet module install -i /etc/puppet/environments/production/modules jfryman-nginx
    #sudo puppet module install -i /etc/puppet/environments/production/modules puppetlabs-haproxy
    #sudo puppet module install -i /etc/puppet/environments/production/modules puppetlabs-apache
    #sudo puppet module install -i /etc/puppet/environments/production/modules puppetlabs-java
fi
