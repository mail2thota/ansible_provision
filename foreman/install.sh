#!/bin/bash
#setup repo and manage the installation of foreman
#author:Heri Sutrisno
#email:herygranding@gmail.com
set -e
thisdir=`dirname $0`
source ${thisdir}/hammer_cfg.sh

setBaseRepo(){

    base_name="CentOS-\$releasever - Base"
    base_url="$url_repo/repos/centos/\$releasever/os/\$basearch"
    base_gpgkey="$url_repo/repos/pki/\$basearch/RPM-GPG-KEY-CentOS-7"
    update_name="CentOS-\$releasever - Updates"
    update_url="$url_repo/repos/centos/\$releasever/updates/\$basearch"
    update_gpgkey="$url_repo/repos/pki/\$basearch/RPM-GPG-KEY-CentOS-7"


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

setCentosSCLO(){

    sclo_name="CentOS-7 - SCLo sclo"
    sclo_url="$url_repo/repos/centos/\$releasever/sclo/\$basearch/sclo"
    sclo_gpgkey="$url_repo/repos/pki/\$basearch/RPM-GPG-KEY-CentOS-SIG-SCLo"

tee /etc/yum.repos.d/CentOS-SCLo-scl.repo <<EOF
[centos-sclo-sclo]
name=$sclo_name
enabled=1
gpgcheck=1
gpgkey=$sclo_gpgkey
baseurl=$sclo_url
EOF
}

setCentosSCLORH(){

    sclorh_name="CentOS-7 - SCLo rh"
    sclorh_url="$url_repo/repos/centos/\$releasever/sclo/\$basearch/rh"
    sclorh_gpgkey="$url_repo/repos/pki/\$basearch/RPM-GPG-KEY-CentOS-SIG-SCLo"

tee /etc/yum.repos.d/CentOS-SCLo-scl-rh.repo <<EOF
[centos-sclo-rh]
name=$sclorh_name
enabled=1
gpgcheck=1
gpgkey=$sclorh_gpgkey
baseurl=$sclorh_url
EOF
}

setEpelRepo(){

    epel_name="Extra Packages for Enterprise Linux 7 - \$basearch"
    epel_url="$url_repo/repos/epel/\$releasever/\$basearch"
    epel_gpgkey="$url_repo/repos/pki/\$basearch/RPM-GPG-KEY-EPEL-7"

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
    foreman_gpgkey="$url_repo/repos/pki/\$basearch/RPM-GPG-KEY-foreman"

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
    foreman_plugin_gpgkey="$url_repo/repos/pki/\$basearch/RPM-GPG-KEY-foreman"

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
    puppet_gpgkey1="$url_repo/repos/pki/\$basearch/RPM-GPG-KEY-puppetlabs-PC1"
    puppet_gpgkey2="$url_repo/repos/pki/\$basearch/RPM-GPG-KEY-puppet-PC1"

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

setHostName(){

    env_label="development"
    if [ "${environment,,}" = "${env_label,,}" ];
    then

        systemctl stop firewalld
        systemctl disable firewalld
        sudo sed -i 's/enforcing/permissive/g' /etc/sysconfig/selinux 
        sudo setenforce 0
        unset http_proxy
        unset https_proxy
        unset no_proxy
        systemctl restart network
    fi
    
    host_ip=$(ip addr show $dhcp_interface | grep -Po 'inet \K[\d.]+')
    echo "127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4" > /etc/hosts
    echo "::1         localhost localhost.localdomain localhost6 localhost6.localdomain6" >> /etc/hosts
    echo "$host_ip $dns_id" >> /etc/hosts
    sudo systemctl restart network
}

installForeman(){
    
    sudo yum -y install foreman-installer nmap

}

setBaseRepo
setCentosSCLO
setCentosSCLORH
setEpelRepo
setForemanRepo
setForemanPluginRepo
setPuppetRepo
setHostName
installForeman

exit 0
