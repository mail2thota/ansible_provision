
# Foreman And Bare Metal Provisioning

Automated provisioning using foreman configuration as easy as pie.
This script automatically help you to automate the installation of foreman, bring
up DHCP server, TFTP server, and DNS local server.
creating resources such as set up multiple subnets, domains, create hosts base on
group, create hosts for provisioning, architectures of machine to be provisioned,
installation medias, set ptable hardisk partition through the kick starter script,
and set the operating system image to be installed.

Prerequisite
------------

    1. setup SE Linux permissive or disabled
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
    4. making sure your DNS address is able to be resolved
        - you may check on /etc/resolv.conf
        - if not set yet you may set manually or you may using nmtui,
            - type "nmtui" you may use arrows, space and enter to navigate the cursor
            - choose "Edit a connection", click enter
            - choose your ethernet interface, click enter e.g; enp0s3
            - choose IPv4 CONFIGURATION set "Automatic", click enter
            - choose Automatically connect, click space
            - click 'OK', and following by click "back" to close the nmtui windows.
            - restart network; "systemctl restart network"
    5. making sure that you don't have any DHCP server available which is been connecting to the subnet network
    6. making sure that your network device interface or network interface e.g; "enp0s3" is dedicated only for single IP(on the future we are going to support single network interface may have multiple IP )

Configuration
-------------

| Variable       |  Example           | Description  |
|:------------- |:-------------|:-----|
|auth:[fqdn,ip,user,pass]|[fqdn:foreman.example.com],[ip:10.11.12.7],[user:admin],[pass:bae4533]|[fqdn:fqdn of foreman],[ip:ip of foreman],[user: user of foreman],[pass:password of foreman]|
|domain:[name,fullname]|[name:baesystemdemo.com],[fullname:full description]|[name:valid domain name],[fullname:clear description]|
|subnet:[name,network,mask,gateway,dns-primary,dns-secondary,vlanid,domain:[name]]|[name:subnet1012],[network:10.11.12.0],[mask:255.255.255.0],[gateway:10.11.12.1],[dns-primary:10.11.12.7],[dns-secondary:8.8.8.8],[vlanid:1],[domain:[name:example.com]]|[name:name of subnet(str,required)],[network:valid of subnet network ip(str,required)],[mask:valid of mask address(str,required)],[gateway:valid of gateway address(str,optional)],[dns-primary:valid of dns ip(str,optional)],[dns-secondary:valid of dns ip(str,optional)],[vlanid:valid of vlanid(int,optional)],[domain:[name:domain name(str,required)]]|
|hostgroup:[name,subnet,domain,root-pass]|[name:hostg_master],[subnet:subnet1012],[domain:example.com],[root-pass:abs12232]|[name:name of hostgroup(str,required)],[subnet:name of subnet to be assigned(str,required)],[domain:name of domain to be assigned(str,required)],[root-pass:default password of nodes(str,required,minimum 8 char)]|
|hosts:[name,hostgroup,ip,mac]|[name:agent_node],[hostgroup:hostg_master],[ip:10.11.12.4],[mac:080027d487f5]|[name:host name(str,required)],[hostgroup:assigned host group(str,required)],[ip:valid of host ip(str,required)],[mac:valid mac address(str,required)]|
|architecture(system default):[name]|[name:x86_64]|[name:currently the only available options is x86_64]|
|medium(system default):[name,path,os-family]|[name:Centos7],[path:http://10.129.6.237/repos/CentOS_7_x86_64/],[os-family:RedHat]|[name:name of os(str,required)],[path:location of image(str,required)],[os-family:type of os(str,required)|
|setting(system default):[name,value]|[name:token_duration],[value:0]|[name:name of foreman variable setting(str,required)],[value:value assigned(int/str,required)]|
|os(system default):[name,major,minor,description,family,release-name,password-hash,architectures:[name],provisioning-template:[name],medium:[name],partition-table:[name],parameters:[version,codename]]|[name:centos7],[major:7],[minor:6],[description:centos7dvd],[family:RedHat],[release-name:centos7release],[password-hash:SHA512],[architectures:[name:x86_64]],[provisioning-template:[name:Kickstart default],[name:Kickstart default finish],[name:Kickstart default PXELinux],[name:Kickstart default iPXE],[name:Kickstart default user data]],[medium:[name:CentOS7]],[partition-table:[name:Kickstart default]],[parameters:[version:7],[codename:Centos7]]|[name:name of os(str,required)],[major:major of version(str,required)],[minor:minor of version(str,required)],[description:details description(str,optional)],[family:family of os(str,optional)],[release-name:name release version(str,optional)],[password-hash:hass password(str,optional)],[architectures:[name:name of architectures(str, optional)]],[provisioning-template:[name:name of provisioning-template(str,optional)],[name:name of provisioning-template(str,optional)],[name:name of provisioning-template(str,optional)],[name:name of provisioning-template(str,optional)],[name:name of provisioning-template(str,optional)]],[medium:[name:name of medium assigned(str,optional)]],[partition-table:[name:name of partition-table assigned(str,optional)]],[parameters:[version:additional info(str,optional)],[codename:additional info(str,optional)]]|
|hostgroup_default(system default):[name,parent,os,architecture,medium,partition-table]|[name:host default],[parent:host default],[os:centos7],[architecture:x86_64],[medium:Centos7],[partition-table:Kickstart default]|[name:name of host assigned(str,required)],[parent:inherit from which parent hostgroup(str,required,can be empty)],[os:os assigned(str,required)],[architecture:architecture assigned(str,required)],[medium:medium assigned(str,required)],[partition-table:partition table assigned(str,required)]
|device_identifier(system default):[name]|[name:enp0s3]|[name:name of valid device identifier(str,optional)]|


Complete YAML User Template
-------------------------------------
User is allowed to modified as they like according requirement to do provisiong process.

    foreman:
        auth:
            fqdn: foreman.example.com
            ip: 10.11.12.5
            user: admin
            pass: as123

        domain:
            - name: example.com
              fullname: this is example.com

        subnet:
            - name: subnet1
              network: 10.11.12.0
              mask: 255.255.255.0
              gateway: 10.11.12.1
              dns-primary: 10.11.12.7
              dns-secondary: 8.8.8.8
              vlanid:
              domain:
                - name: example.com

        hostgroup:
            - name: master
              subnet: subnet1
              domain: example.com
              root-pass: as12345678

        hosts:
            - name: agent1
              hostgroup: master
              ip: 10.11.12.05
              mac: 080027d487f5


Complete YAML System Default Template
-------------------------------------
It is restricted for user making changes on system.yml file below, but it is configurable and allow to be modified as per user need. You may find it in /etc/foreman_client/config/system.yml.

    foreman:
        architecture:
            - name: x86_64

        medium:
            - name: CentOS7
              path: http://10.129.6.237/repos/CentOS_7_x86_64/
              os-family: Redhat

        setting:
            - name: token_duration
              value: 0
        os:
            - name: centos7
              major: 7
              minor: 6
              description: centos7
              family: Redhat
              release-name: centos7_release1
              password-hash: SHA512
              architecture:
                - name: x86_64
              provisioning-template:
                - name: Kickstart default
                - name: Kickstart default finish
                - name: Kickstart default PXELinux
                - name: Kickstart default iPXE
                - name: Kickstart default user data
              medium:
                - name: CentOS7
              partition-table:
                - name: Kickstart default
              parameters:
                version: "7"
                codename: "centos7"

        hostgroup_default:
              - name: host default
                parent:
                os: centos7
                architecture: x86_64
                medium: CentOS7
                partition-table: Kickstart default

        device_identifier:
              - name: enp0s3


Installation and Provisioning Foreman
-------------------------------------

    git clone ssh://git@10.37.0.35:7999/ta/mdr_platform_bare_metal.git
    cd foreman
    ./boot.sh

    noted:when you see provisioning is ready you might turn up the nodes to be provisioned,
    from bios setting you may choose boot from network and allow boot using PXELinux



Usage
-----
    run as standalone provisioning:
    1. Install using tar:
        * su root
        * pip install fmclient-0.0.1.tar.gz
    2. install from source:
        * su root
        * checkout : git clone ssh://git@10.37.0.35:7999/ta/mdr_platform_bare_metal.git
        * cd foreman_yml
        * pip install -e .                      
    2. import YAML file: fmclient import /path/filename.yml
    3. turn on/restart your nodes for provisioning setup
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
