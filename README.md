
# Foreman And Bare Metal Provisioning

Automated provisioning using foreman configuration as easy as pie.
This script automatically help you to automate the installation of foreman, bring
up DHCP server, TFTP server, and DNS local server.
creating resources such as set up multiple subnet, domain, create host base on
group, create hosts for provisioning, architecture of machine to be provisioned,
installation media, set ptable hardisk partition through kick starter script,
and set the operating system image to be installed.

Prerequisite
------------

    1. setup SE Linux permissive
            /etc/sysconfig/selinux
    2. set-up firewall or disable it
            - disable
                sudo systemctl stop firewalld
                sudo systemctl disable firewalld
            - allow to go through
                sudo firewall-cmd --permanent --add-service=http
                sudo firewall-cmd --permanent --add-service=https
                sudo firewall-cmd --permanent --add-port=69/tcp
                sudo firewall-cmd --permanent --add-port=67-69/udp
                sudo firewall-cmd --permanent --add-port=53/tcp
                sudo firewall-cmd --permanent --add-port=53/udp
                sudo firewall-cmd --permanent --add-port=8443/tcp
                sudo firewall-cmd --permanent --add-port=8140/tcp
	3. http repo setup on bootstrap machine
			- installation of nginx Repo
				https://engineering/bitbucket/projects/TA/repos/mdr_platform_bare_metal/browse/nginx
    4. making sure your DNS address is resolved
        - you may check on /etc/resolv.conf
        - if not set yet you may set manually or you may using nmtui,
            - type "nmtui" you may use arrows, space and enter to navigate cursor
            - choose "Edit a connection", click enter
            - choose your ethernet interface, click enter e.g; enp0s3
            - choose IPv4 CONFIGURATION set "Automatic", click enter
            - choose Automatically connect, click space
            - click ok follow by click back to close the nmtui windows.
            - restart network; systemctl restart network
Configuration
-------------

| Variable       |  Example           | Description  |
|:------------- |:-------------|:-----|
|username|admin|User name of the foreman|
|password|as1123|password for the foreman|
|architecture|x86_64|The available options are i386 and x86_64|
|domain|baesystemdemo.com|valid domain name|
|url_repo|http://10.129.6.142|resolveable url for local repo|
|dns_name|foreman.baesystemdemo.com|valid dns name|
|host_ip|10.129.6.189|ip for the host bootstrap machine check by using ifconfig or ip addr|
|medium_name|CentOSDemo7|name for medium|
|image_path|http://10.129.6.142|address where image reside, you may use ftp or http only|
|os_name|CentOSDemo7|name of os to be provisioned|
|os_majorversion|7|max possibility for os version to be installed|
|os_minorversion|2|minimum possibility os version to be installed|
|os_family|RedHat|os family such as RedHat or Debian|
|template_default|Kickstart default|default provisioning template for RedHat|
|template_finish|Kickstart default finish|default provisioning template for RedHat|
|template_ipxe|Kickstart default iPXE|default provisioning template for RedHat|
|template_pxelinux|Kickstart default PXELinux|default provisioning template for RedHat|
|template_userdata|Kickstart default user data|default provisioning template for RedHat|
|subnet_name|baesystemSubnet|profile name to set subnet|
|subnet_network|10.11.12.0|ip address for the subnet|
|subnet_mask|255.255.255.0|subnet mask|
|subnet_gateway|10.11.12.1|gateway address|
|subnetip_start|10.11.12.1|the range of start IP that will be served by subnet|
|subnetip_end|10.11.12.24|the range of end IP that will be served by subnet|
|dhcp_interface|enp0s3|it is network interface, you may check by using ifconfig or ip addr|
|environment|production|labeling environment status, production or development|
|host_groupname|ambari_group|name for hostgroup|
|node_pass|as021d90j@|default password to be set on nodes upon OS provisioning|
|numbers_of_node|4|total number of nodes|
|number_of_master|2|specify numbers of node for master|
|number_of_agent|4|specify numbers of node for agent|
|master+(1-n)|master1|specify mac address for master node, follow the sequence 1-n in integer format|
|agent+(1-n)|agent1|specify mac address for master node, follow the sequence 1-n in integer format|




Installation and Provisioning Foreman
-------------------------------------

    git clone ssh://git@10.37.0.35:7999/ta/mdr_platform_bare_metal.git
    cd foreman
    ./boot.sh

    noted:when you see provisioning is ready you might turn up the nodes to be provisioned,
    from bios setting you may choose boot from network and allow boot using PXELinux


Log
---

    trace log through tail -f /var/log/foreman-installer/foreman.log

Installation Of Ansible
-----------------------

    https://engineering/bitbucket/projects/TA/repos/mdr_platform_bare_metal/browse/ansible

Installation Of Ambari
----------------------

    https://engineering/bitbucket/projects/TA/repos/mdr_platform_bare_metal/browse/ambari

HDP Cluster
----------------------

    https://engineering/bitbucket/projects/TA/repos/mdr_platform_bare_metal/browse/hdp/blueprints


License
-------

@BaeSystemsAI
