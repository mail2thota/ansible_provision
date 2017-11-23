
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
	  3. local http repo and pypi repo setup on bootstrap machine
	        - installation of nginx Repo
	              https://engineering/bitbucket/projects/TA/repos/mdr_platform_bare_metal/browse/nginx
          - installation of pypi
                * pypy should be install in sameplace where http repo installed.
                * install pip: yum -y install python-pip
                * install pypi server:pip install pypiserver
                * unzip file: tar xvfz packages.tar.gz ~/
                * run command: nohup pypi-server -p 8008 -P . -a . ~/packages/ &
                * verify by using curl or open browser http://repo_url:8008/packages
                * pypi local repo must be bind using port 8008.
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
    7. make sure your proxy is disable, check as well in /etc/yum.conf
    8. ansible version required is : ansible 2.3.1.0
    9. The best approach is for having static ip for bootstrap machine, check how to setup static ip below:
--------------
Static IP
-------------
    #static ip for bootstrap machine:
    #cat /etc/sysconfig/network-scripts/ifcfg-enp0s3

    BOOTPROTO="none"
    IPADDR="10.11.12.7"
    NETMASK="255.255.255.0"
    GATEWAY="10.11.12.1"
    DEVICE=enp0s3
    HWADDR="08:00:27:78:b1:a1"
    ONBOOT=yes
    PEERDNS=yes
    PEERROUTES=yes
    DEFROUTE=yes
    DNS1="10.11.12.7"



Configuration
-------------

| Variable       |  Example           | Description  |
|:------------- |:-------------|:-----|
|auth:[fqdn,ip,user,pass]|[fqdn:foreman.example.com],[ip:10.11.12.7],[user:admin],[pass:bae4533]|[fqdn:fqdn of foreman(resolvable of fqdn,required)],[ip:ip of foreman(valid ip,required)],[user: user of foreman(string, required)],[pass:password of foreman(string, required)]|
|domain:[name,fullname]|[name:baesystemdemo.com],[fullname:full description]|[name:valid of domain's name(str,required)],[fullname:clear of description(str,optional)]|
|subnet:[name,network,mask,gateway,dns-primary,dns-secondary,vlanid,domain:[name]]|[name:subnet1012],[network:10.11.12.0],[mask:255.255.255.0],[gateway:10.11.12.1],[dns-primary:10.11.12.7],[dns-secondary:8.8.8.8],[vlanid:1],[domain:[name:example.com]]|[name:name of subnet(str,required)],[network:valid of subnet network ip(str,required)],[mask:valid of mask address(str,required)],[gateway:valid of gateway address(str,optional)],[dns-primary:valid of dns ip(str,optional)],[dns-secondary:valid of dns ip(str,optional)],[vlanid:valid of vlanid(int,optional)],[domain:[name:domain name(str,required)]]|
|hostgroup:[name,subnet,domain,root-pass]|[name:hostg_master],[subnet:subnet1012],[domain:example.com],[root-pass:abs12232]|[name:name of hostgroup(str,required)],[subnet:name of subnet to be assigned(str,required)],[domain:name of domain to be assigned(str,required)],[root-pass:default password of nodes(str,required,minimum 8 char)]|
|hosts:[name,hostgroup,ip,mac]|[name:agent_node],[hostgroup:hostg_master],[ip:10.11.12.4],[mac:080027d487f5]|[name:host name(str,required)],[hostgroup:assigned host group(str,required)],[ip:valid of host ip(str,required)],[mac:valid mac address(str,required)]|
|architecture(system default):[name]|[name:x86_64]|[name:currently the only available options is x86_64]|
|medium(system default):[name,path,os-family]|[name:Centos7],[path:http://10.129.6.237/repos/CentOS_7_x86_64/],[os-family:RedHat]|[name:name of os(str,required)],[path:location of image(str,required)],[os-family:type of os(str,required)|
|setting(system default):[name,value]|[name:token_duration],[value:0]|[name:name of foreman variable setting(str,required)],[value:value assigned(int/str,required)]|
|os(system default):[name,family,password-hash,architectures:[name],provisioning-template:[name],medium:[name],partition-table:[name]]|[name:centos7],[family:RedHat],[password-hash:SHA512],[architectures:[name:x86_64]],[provisioning-template:[name:Kickstart default],[name:Kickstart default finish],[name:Kickstart default PXELinux],[name:Kickstart default iPXE],[name:Kickstart default user data]],[medium:[name:CentOS7]],[partition-table:[name:Kickstart default]]|[name:name of os(str,required)],[family:family of os(str,optional)],[password-hash:hash password(str,optional)],[architectures:[name:name of architectures(str, optional)]],[provisioning-template:[name:name of provisioning-template(str,optional)],[name:name of provisioning-template(str,optional)],[name:name of provisioning-template(str,optional)],[name:name of provisioning-template(str,optional)],[name:name of provisioning-template(str,optional)]],[medium:[name:name of medium assigned(str,optional)]],[partition-table:[name:name of partition-table assigned(str,optional)]|
|hostgroup_default(system default):[name,parent,os,architecture,medium,partition-table]|[name:host default],[parent:host default],[os:centos7],[architecture:x86_64],[medium:Centos7],[partition-table:Kickstart default]|[name:name of host assigned(str,required)],[parent:inherit from which parent hostgroup(str,required,can be empty)],[os:os assigned(str,required)],[architecture:architecture assigned(str,required)],[medium:medium assigned(str,required)],[partition-table:partition table assigned(str,required)]
|device_identifier(system default):[name]|[name:enp0s3]|[name:name of valid device identifier(str,optional)]|
|timeout_second|timeout_second: 172800|find it in /foreman-ansible/ansible/roles/fmclient/defaults/main.yml. it is timeout(format in second) for foreman waiting to finish node provisioning, default is set for 48 hours waiting for foreman to finish node provisioning.


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
It is restricted for user making changes on system.yml file below, but it is configurable and allow to be modified as per user need. before provisioning You may find it in /foreman-ansible/ansible/roles/fmclient/templates/system.yml.j2.

    foreman:
        architecture:
            - name: x86_64

        medium:
            - name: CentOS7_x86_64
              path: http://10.129.6.237/repos/CentOS_7_x86_64/
              os_family: Redhat

        setting:
            - name: token_duration
              value: 360
              protocol: http

        os:
            - name: CentOS7
              family: Redhat
              password_hash: SHA512
              architecture:
                - name: x86_64
              provisioning_template:
                - name: Kickstart default
                - name: Kickstart default finish
                - name: Kickstart default PXELinux
                - name: Kickstart default iPXE
                - name: Kickstart default user data
              medium:
                - name: CentOS7_x86_64
              partition_table:
                - name: Kickstart default

        hostgroup_default:
              - name: hostg_default
                parent:
                os: CentOS7
                architecture: x86_64
                medium: CentOS7_x86_64
                partition_table: Kickstart default

        device_identifier:
              - name: enp0s3



Installation and Provisioning Foreman
-------------------------------------

    git clone ssh://git@10.37.0.35:7999/ta/mdr_platform_bare_metal.git
    * cd /foreman-ansible/ansible
    * configure:
          - /foreman-ansible/ansible/templates/payload.yml
          - /foreman-ansible/ansible/bootup.sh
     * set correct url_repo in /foreman-ansible/ansible/bootup.sh

    * launch:
          - cd /foreman-ansible/ansible/
          - ./bootup.sh

    noted:when you see provisioning is ready you might turn up the nodes to be provisioned,
    from bios setting you may choose boot from network and allow boot using PXELinux. After the installation You may find the rest of log and setting in /opt/foreman_yml/ for the further chanages


---

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
