#!/bin/bash

url_repo="http://10.129.6.142"

setBaseRepo(){

    base_name="CentOS-\$releasever - Base"
    base_url="$url_repo/repos/centos/\$releasever/os/\$basearch"
    base_gpgkey="$url_repo/repos/centos/\$releasever/os/\$basearch/RPM-GPG-KEY-CentOS-7"
    update_name="CentOS-\$releasever - Updates"
    update_url="$url_repo/repos/centos/\$releasever/updates/\$basearch"
    update_gpgkey="$url_repo/repos/centos/\$releasever/os/\$basearch/RPM-GPG-KEY-CentOS-7"


tee /etc/yum.repos.d/CentOS-Base.repo <<EOF
[base]
name=$base_name
gpgcheck=1
gpgkey=$base_gpgkey
baseurl=$base_url

[update]
name=$update_name
gpgcheck=1
gpgkey=$update_gpgkey
baseurl=$update_url
EOF
}

setEpelRepo(){

    epel_name="Extra Packages for Enterprise Linux 7 - \$basearch"
    epel_url="$url_repo/repos/epel/\$releasever/\$basearch"
    epel_gpgkey="file:///foreman_installer/pki/RPM-GPG-KEY-EPEL-7"

tee /etc/yum.repos.d/epel.repo <<EOF
[epel]
name=$epel_name
enabled=1
gpgcheck=1
gpgkey=$epel_gpgkey
baseurl=$epel_url
EOF
}

setForemanRepo(){

    foreman_name="Foreman 1.15 - source"
    foreman_url="$url_repo/repos/foreman/1.15/el7/\$basearch"
    foreman_gpgkey="file:///foreman_installer/pki/RPM-GPG-KEY-foreman"

tee /etc/yum.repos.d/foreman.repo <<EOF
[foreman]
name=$foreman_name
baseurl=$foreman_url
enabled=1
gpgcheck=1
gpgkey=$foreman_gpgkey
EOF
}

setForemanPluginRepo(){

    foreman_plugin_name="Foreman plugins 1.15"
    foreman_plugin_url="$url_repo/repos/foreman_plugin/1.15/el7/\$basearch"
    foreman_plugin_gpgkey="file:///foreman_installer/pki/RPM-GPG-KEY-foreman"

tee /etc/yum.repos.d/foreman-plugins.repo <<EOF
[foreman-plugins]
name=$foreman_plugin_name
baseurl=$foreman_plugin_url
enabled=1
gpgcheck=0
gpgkey=$foreman_plugin_gpgkey
EOF
}

setPuppetRepo(){

    puppet_name="Puppet Labs PC1 Repository el 7 - \$basearch"
    puppet_url="$url_repo/repos/puppet/el/7/PC1/\$basearch"
    puppet_gpgkey1="file:///foreman_installer/pki/RPM-GPG-KEY-puppetlabs-PC1"
    puppet_gpgkey2="file:///foreman_installer/pki/RPM-GPG-KEY-puppet-PC1"

tee /etc/yum.repos.d/puppetlabs-pc1.repo <<EOF
[puppetlabs-pc1]
name=$puppet_name
baseurl=$puppet_url
gpgkey=$puppet_gpgkey1
       $puppet_gpgkey2
enabled=1
gpgcheck=1
EOF
}

installForeman(){

sudo yum -y install foreman-installer nmap-ncat 
sudo yum -y install tfm-rubygem-hammer_cli_foreman_discovery

}
setBaseRepo
setEpelRepo
setForemanRepo
setForemanPluginRepo
setPuppetRepo
exit 1
installForeman

