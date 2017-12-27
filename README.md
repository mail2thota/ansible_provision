
# Foreman And Bare Metal Provisioning

Automated provisioning using foreman configuration as easy as pie.
This solution automatically help you to automate the installation of foreman on premises, bringing
up DHCP server, TFTP server, and DNS local server.
Creating resources such as set up multiple subnets, domains, create hosts base on
group, create hosts for provisioning, architectures of machine to be provisioned,
installation medias, set ptable hardisk partition through the kick starter script,
and set the operating system image to be installed. All of process take place in bare metal environment and configuration file must be set in YML format.

Prerequisite
------------

    1. Setup SE Linux permissive or disabled
          - modified: /etc/sysconfig/selinux
          - restart machine

    2. Setup firewall or disable it
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
                sudo firewall-cmd --permanent --add-port=5432/tcp
                sudo firewall-cmd --permanent --add-port=8443/tcp

	  3. Install local yum and pypi Repository setup on bootstrap machine

          - installation of Nginx Repository
	              https://engineering/bitbucket/projects/TA/repos/mdr_platform_bare_metal/browse/nginx

          - installation of pypi
                * pypi should be installed in sameplace where http repository was installed.
                * install pip:
                      yum -y install python-pip
                * install pypi server:
                      pip install pypiserver
                * download packages.tar.gz :
                      wget -N http://10.129.6.237/repos/repo_share/packages.tar.gz
                * unzip file:
                      tar xvfz packages.tar.gz ~/
                * run command:
                      nohup pypi-server -p 8008 -P . -a . ~/packages/ &
                * verify by using curl or open browser:
                      http://repo_url:8008/packages
                * pypi local repository must be bind using port 8008.

    4. If DNS required, Making sure your DNS address is resolveable
          - you may check on:
                 /etc/resolv.conf
          - if not set yet you may set manually or you may configure using nmtui,
                - type "nmtui" you may use arrows, space and enter to navigate the cursor
                - choose "Edit a connection", click enter
                - choose your ethernet interface, click enter e.g; enp0s3
                - choose IPv4 CONFIGURATION set "Automatic", click enter
                - choose Automatically connect, click space
                - click 'OK', and following by click "back" to close the nmtui windows.
                - restart network; "systemctl restart network"

    5. Making sure that you don't have any DHCP server available which is been connecting to the subnet network

    6. Making sure that your network device interface or network interface in bootstrap machine e.g; "eth0" is
       dedicated only for single Ip

    7. Make sure your http_proxy and https_proxy is disabled, check as well in /etc/yum.conf

    8. If you have existing Ansible, Required Ansible version : ansible 2.3.1.0

    9. The best approach is for having static Ip for bootstrap machine, check how to setup static Ip below:
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
|auth: <ul><li>**foreman_fqdn**</li><li>**foreman_ip**</li><li>**foreman_user**</li><li>**foreman_pass**</ul></li>|<ul><li>**foreman_fqdn:** foreman.example.com</li><li>**foreman_ip:** 10.11.12.7</li><li>**foreman_user:** admin</li><li>**foreman_pass:** bae4533</li></ul>|<ul><li>**foreman_fqdn:** fqdn of foreman(resolvable of fqdn, required)</li><li>**foreman_ip:** ip of bootstrap machine(valid ip, required)</li><li>**foreman_user:** user name of foreman(string, required)</li><li>**foreman_pass:** password of foreman(string, required)</li></ul>|
|domain: <ul><li>**name**</li><li>**fullname**</li></ul>|<ul><li>**name:** baesystemdemo.com</li><li>**fullname:** full description</li></ul>|<ul><li>**name:** valid of domain's name(str, required)</li><li>**fullname:** clear of description(str, optional)</li></ul>|
|subnet:<ul><li>**name**</li><li>**network**</li><li>**mask**</li><li>**gateway**</li><li>**dns-primary**</li><li>**dns-secondary**</li><li>**vlanid**</li><li>**domain:**<ul><li>**name**</ul></li></ul></li>|<ul><li>**name:** subnet1012</li><li>**network:** 10.11.12.0</li><li>**mask:** 255.255.255.0</li><li>**gateway:** 10.11.12.1</li><li>**dns-primary:** 10.11.12.7</li><li>**dns-secondary:** 8.8.8.8</li><li>**vlanid:** 1</li><li>**domain:**  <ul><li>**name:** example.com</li></ul></li></ul>|<ul><li>**name:** name of subnet(str, required)</li><li>**network:** valid of subnet network ip(str, required)</li><li>**mask:** valid of mask address(str, required)</li><li>**gateway:** valid of gateway address(str, optional)</li><li>**dns-primary:** valid of dns ip(str, optional)</li><li>**dns-secondary:** valid of dns ip(str, optional)</li><li>**vlanid:** valid of vlanid(int, optional)</li><li>**domain:** <ul><li>**name:** domain name(str, required)</li></ul></li></ul>|
|partition_table:<ul><li>**name**</li><li>**boot:**<ul><li>**fstype**</li></ul><ul><li>**size**</li></ul></li><li>**swap:** <ul><li>**fstype**</li></ul><ul><li>**size**</li></ul></li><li>**tmp:** <ul><li>**fstype**</li></ul><ul><li>**size**</li></ul></li><li>**var:** <ul><li>**fstype**</li></ul><ul><li>**size**</li></ul></li><li>**home:** <ul><li>**fstype**</li></ul><ul><li>**size**</li></ul></li><li>**root:** <ul><li>**fstype**</li></ul><ul><li>**size**</li></ul></li></ul>|<ul><li>**name**</li><li>**boot:**<ul><li>**fstype:** ext2</li></ul><ul><li>**size:** 10</li></ul></li><li>**swap:**<ul><li>**fstype:** swap</li></ul><ul><li>**size:** 10</li></ul></li><li>**tmp:** <ul><li>**fstype:** ext4</li></ul><ul><li>**size:** 10</li></ul></li><li>**var:** <ul><li>**fstype:** xfs</li></ul><ul><li>**size:** 10</li></ul></li><li>**home:** <ul><li>**fstype:** ext4</li></ul><ul><li>**size:** 10</li></ul></li><li>**root:** <ul><li>**fstype:** ext4</li></ul><ul><li>**size:** 50</li></ul></li></ul>| <ul><li>**name**</li><li>**boot:** boot partition</li><li>**swap:** swap partition</li><li>**tmp:** tmp partition </li><li>**var:** var partition</li><li>**home:** home partition</li><li>**root:** root partition</li><li>**fstype:** file system type</li><li>**size:** size in percentage format</li><li>**noted:** <ul><li>**partition support:** xfs,ext2,ext3,ext4, swap for swap</li></ul><ul><li>**size:** size must be in percentage digit and total accumulation size must be 100%</li></ul></li></ul>
|hostgroup_system:<ul><li>**os**</li><li>**architecture**</li><li>**medium**</li></ul>|<ul><li>**os:** centos7</li><li>**architecture:** x86_64</li><li>**medium:** Centos7</li></ul>|<ul><li>**os:** assign operating system name(str, required)</li><li>**architecture:** assign architecture name (str, required)</li><li>**medium:** assign medium name(str, required)</li></ul>
|hostgroup:<ul><li>**name**</li><li>**subnet**</li><li>**domain**</li><li>**root-pass**</li><li>**partition_table**</li></ul>|<ul><li>**name:** hostg_master</li><li>**subnet:** subnet1012</li><li>**domain:** example.com</li><li>**root-pass:** abs12232</li><li>**partition_table:** Kickstart default</li></ul>|<ul><li>**name:** name of hostgroup(str, required)</li><li>**subnet:** name of subnet to be assigned(str, required)</li><li>**domain:** name of domain to be assigned(str, required)</li><li>**root-pass:** default password of nodes(str, required, minimum 8 char)</li><li>**partition_table:** name of partition table to be assigned(str, required)</li></ul>|
|primary_hosts:<lu><li>**name**</li><li>**hostgroup**</li><li>**ip**</li><li>**mac**</li></lu>|<ul><li>**name:** agent_node</li><li>**hostgroup:** hostg_master</li><li>**ip:** 10.11.12.4</li><li>**mac:** 080027d487f5</li></ul>|<ul><li>**name:** host name(str, required)</li><li>**hostgroup:** assign host group(str, required)</li><li>**ip:** valid of host ip(str, required)</li><li>**mac:** valid of mac address(str, required)</li></ul>|
|secondary_hosts:<lu><li>**ip**</li><li>**mac**</li><li>**subnet**</li><li>**primary**</li></lu>|<lu><li>**ip:** 10.11.12.6</li><li>**mac:** 080027F8D3E8</li><li>**subnet:** subnet1012</li><li>**primary:** agent_node</li></lu>|<ul><li>**ip:** ip address, must be unique(str, required)</li><li>**mac:** mac address, must be unique(str, required)</li><li>**subnet:** valid subnet to be assigned(str, required)</li><li>**primary:** valid primary node name to be assigned(str, required)</li></ul>|
|protocol: <ul><li>**type**</li></ul>|<ul><li>**type:** http</li></ul>|<ul><li>**type:** only support http(str, required)</li></ul>|
|foreman_proxy: <ul><li>**port**</li></ul>|<ul><li>**port:** 8443</li></ul>|<ul><li>**port:** port of foreman_proxy(int, required)</li></ul>|
|architecture:<ul><li>**name**</li></ul>|<ul><li>**name:** x86_64</li></ul>|<ul><li>**name:** currently only support x86_64 version</lu></ul>|
|medium:<ul><li>**name**</li><li>**path**</li><li>**os-family**</li></ul>|<ul><li>**name:** Centos7</li><li>**path:** /repos/CentOS_7_x86_64/</li><li>**os-family:** RedHat</li></ul>|<ul><li>**name:** name of os(str, required)</li><li>**path:** location of image(str, required)</li><li>**os-family:** type of os(str, required)</li></ul>|
|setting:<ul><li>**name**</li><li>**value**</ul></li>|<ul><li>**name:** token_duration</li><li>**value:** 0 </li></ul>|<ul><li>**name:** name of foreman variable setting(str, required)</li><li>**value:** value to be assigned(int/str, required)</li></ul>|
|os:<ul><li>**name**</li><li>**family**</li><li>**password-hash**</li><li>**architectures:** <ul><li>**name:**</li></ul></li><li>**provisioning-template:** <ul><li>**name:**</li></ul></li><li>**medium:** <ul><li>**name**</li></ul></li></ul>|<ul><li>**name:** centos7</li><li>**family:** RedHat</li><li>**password-hash:** SHA512</li><li>**architectures:** <ul><li>**name:** x86_64</li></ul></li><li>**provisioning-template:** <ul><li>**name:** Kickstart default</li></ul><ul><li>**name:** Kickstart default finish</li></ul><ul><li>**name:** Kickstart default PXELinux</li></ul><ul><li>**name:** Kickstart default iPXE</li></ul><ul><li>**name:** Kickstart default user data</li></ul></li><li>**medium:**<ul><li>**name:** CentOS7</li></ul>|<ul><li>**name:** name of os(str, required)</li><li>**family:** family of os(str, optional)</li><li>**password-hash:** hash password(str, optional)</li><li>**architectures:** <ul><li>**name:** name of architectures(str, optional)</li></ul></li><li>**provisioning-template:** <ul><li>**name:** name of provisioning-template(str, optional)</li></ul><ul><li>**name:** name of provisioning-template(str, optional)</li></ul><ul><li>**name:** name of provisioning-template(str, optional)</li></ul><ul><li>**name:** name of provisioning-template(str, optional)</li></ul><ul><li>**name:** name of provisioning-template(str, optional)</li></ul></li><li>**medium:** <ul><li>**name:** name of medium assigned(str, optional)</li></ul>|



Complete YAML User Template
-------------------------------------
User is allowed to modified as they like according to requirement to do provisiong process.you may find it in /mdr_platform_bare_metal/ansible/mdr_cluster/config.yml

    common:

      hostgroups:
          - name: ambari
            subnet: subnet1
            domain: example.com
            root_pass: as12345678
            partition_table: Kickstart default

          - name: ambari2
            subnet: subnet1
            domain: example.com
            root_pass: as12345678
            partition_table: Kickstart default


      primary_hosts:

          - name: node1
            hostgroup: ambari
            ip: 10.11.12.4
            mac: 0800271AD0DA

          - name: node2
            hostgroup: ambari
            ip: 10.11.12.5
            mac: 080027626A0D

          - name: node3
            hostgroup: ambari
            ip: 10.11.12.6
            mac: 080027EEF558

          - name: node4
            hostgroup: ambari
            ip: 10.11.12.7
            mac: 08002774D5B0

      secondary_hosts:
          - ip: 10.11.12.8
            mac: 0800279B8DDA
            subnet: subnet1
            primary: node3

          - ip: 10.11.12.9
            mac: 080027F8D3E8
            subnet: subnet1
            primary: node4


    foreman:

        auth:
            foreman_fqdn: bootstrap.example.com
            foreman_ip: 10.11.12.23
            foreman_user: admin
            foreman_pass: admin

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
            - name: subnet2
              network: 13.11.12.0
              mask: 255.255.255.0
              gateway: 13.11.12.1
              dns_primary: 13.11.12.7
              dns_secondary: 8.8.8.8
              vlanid:
              domain:
                - name: example.com

        partition_table:
            - name: Kickstart default
              boot:
                  fstype: ext2
                  size: 10
              swap:
                  fstype: swap
                  size: 10
              tmp:
                  fstype: ext4
                  size: 10
              var:
                  fstype: xfs
                  size: 10
              home:
                  fstype: ext4
                  size: 10
              root:
                  fstype: ext4
                  size: 50
            - name: Kickstart default2
              boot:
                  fstype: ext2
                  size: 10
              swap:
                  fstype: swap
                  size: 10
              tmp:
                  fstype: ext4
                  size: 10
              var:
                  fstype: xfs
                  size: 10
              home:
                  fstype: ext4
                  size: 10
              root:
                  fstype: ext4
                  size: 50



Complete YAML System Default Template
-------------------------------------
It is restricted for user making changes on system.yml file below, but it is configurable and allow to be modified as per user need. before provisioning You may find it in /mdr_platform_bare_metal/ansible/mdr_cluster/fmconfig/system.yml.j2.

    foreman:

        protocol:
              type: http

        foreman_proxy:
              port: 8443

        architecture:
            - name: x86_64

        medium:
            - name: CentOS7_x86_64
              path: /repos/CentOS_7_x86_64/
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

        hostgroup_default:
            - os: CentOS7
              architecture: x86_64
              medium: CentOS7_x86_64

        partition_system:
             disk_minimum: 500
             boot_size: 730
             boot_type: ext2
             swap_size: 8192
             swap_type: swap
             home_size: 5120
             home_type: ext4
             var_size: 102400
             var_type: xfs
             tmp_size: 102400
             tmp_type: ext4
             root_size: 281138
             root_type: ext4  





Installation and Provisioning Foreman
-------------------------------------
    git clone ssh://git@10.37.0.35:7999/ta/mdr_platform_bare_metal.git
    * cd /mdr_platform_bare_metal/ansible/mdr_cluster
    * configure:
          config.yml:
          	- /mdr_platform_bare_metal/ansible/mdr_cluster/config.yml
          system.yml.j2:
            - /mdr_platform_bare_metal/ansible/mdr_cluster/fmconfig/system.yml.j2

    * launch:
          - cd /mdr_platform_bare_metal/ansible/mdr_cluster/
          - ./bootstrap.sh http://repository_ip

    noted:when you see provisioning is ready you might turn up the nodes to be provisioned,
    from bios setting you may choose boot from network and allow boot using PXELinux. After the installation You may find the rest of log and setting in /opt/foreman_yml/ for the further chanages


---

Provisioning MDR Platform
-----------------------

    https://engineering/bitbucket/projects/TA/repos/mdr_platform_bare_metal/browse/ansible


HDP Blueprints (This section contains blueprint design specification and architecture documentation)
----------------------------------------------------------------------------------------------------

    https://engineering/bitbucket/projects/TA/repos/mdr_platform_bare_metal/browse/blueprints
    https://engineering/confluence/display/MSS/Ambari+Blueprint+Design+Specification

Software Versions
-----------------
| Software       | Version        |
| :------------- | :------------- |
| ActiveMQ       |     5.15       |
| Ambari         |     2.5.2      |
| Apache  Tomcat |     7.0.76     |
| CentOS         |     7.1        |
| Elastic Search |     5.5.0      |
| Foreman        |     1.15.13    |
| HDP            |     2.5 & 2.6  |
| Java SE        |     1.8        |
| Kibana         |     5.5.0      |
| MySql          |     5.6.38-2   |
| Python         |     2.7        |
| Python-pip     |     8.1.2      |

Licence
-------

Mdr_Platform_bare_metal - Copyright (c) 2016 BAE Systems Applied Intelligence.
