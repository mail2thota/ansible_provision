
# Bare Metal Provisioning and Cluster Setup

There are two terminologies to be understood before going into actual steps of installation
### Bootstrap machine
Machine which is expected to be fresh, without any software which is going to installed by mdr_platform_bare_metal such as ansible and foreman
### Target  machine
These are the machine which has to be provisioned by foreman and which needed to be installed the softwares such as  activemq,ambari-agent,ambari-server,docker,elasticsearch,httpd,kibana,mongodb,ntp,java,postgresql,python-pip,tomcat,wget, etc. Also all other HDP components for example JOURNALNODE, NAMENODE, etc. Foreman is normally used to install the OS in bare metal machine, this is optional. It can be skipped if the machine is already provisioned.

## Foreman Usage
Automated provisioning using foreman configuration as easy as pie.
This solution automatically help you to automate the installation of foreman on premises, bringing
up DHCP server, TFTP server, and DNS local server.
Creating resources such as set up multiple subnets, domains, create hosts base on
group, create hosts for provisioning, architectures of machine to be provisioned,
installation medias, set ptable hardisk partition through the kick starter script,
and set the operating system image to be installed. All of process take place in bare metal environment and configuration file must be set in YML format.

## Configuration for foreman
-----------------------------

| Variable       |  Example           | Description  |
|:------------- |:-------------|:-----|
|auth: <ul><li>**foreman_fqdn**</li><li>**foreman_ip**</li>|<ul><li>**foreman_fqdn:** foreman.example.com</li><li>**foreman_ip:** 10.11.12.7</li></ul>|<ul><li>**foreman_fqdn:** fqdn of foreman(resolvable of fqdn, required)</li><li>**foreman_ip:** ip of bootstrap machine(valid ip, required)</li></ul>|
|domain: <ul><li>**name**</li><li>**fullname**</li></ul>|<ul><li>**name:** baesystemdemo.com</li><li>**fullname:** full description</li></ul>|<ul><li>**name:** valid of domain's name(str, required)</li><li>**fullname:** clear of description(str, optional)</li></ul>|
|subnet:<ul><li>**name**</li><li>**network**</li><li>**mask**</li><li>**gateway**</li><li>**dns-primary**</li><li>**dns-secondary**</li><li>**vlanid**</li><li>**domain:**<ul><li>**name**</ul></li></ul></li>|<ul><li>**name:** subnet1012</li><li>**network:** 10.11.12.0</li><li>**mask:** 255.255.255.0</li><li>**gateway:** 10.11.12.1</li><li>**dns-primary:** 10.11.12.7</li><li>**dns-secondary:** 8.8.8.8</li><li>**vlanid:** 1</li><li>**domain:**  <ul><li>**name:** example.com</li></ul></li></ul>|<ul><li>**name:** name of subnet(str, required)</li><li>**network:** valid of subnet network ip(str, required)</li><li>**mask:** valid of mask address(str, required)</li><li>**gateway:** valid of gateway address(str, optional)</li><li>**dns-primary:** valid of dns ip(str, optional)</li><li>**dns-secondary:** valid of dns ip(str, optional)</li><li>**vlanid:** valid of vlanid(int, optional)</li><li>**domain:** <ul><li>**name:** domain name(str, required)</li></ul></li></ul>|
|partition_table:<ul><li>**name**</li><li>**boot:**<ul><li>**fstype**</li></ul><ul><li>**size**</li></ul></li><li>**swap:** <ul><li>**fstype**</li></ul><ul><li>**size**</li></ul></li><li>**tmp:** <ul><li>**fstype**</li></ul><ul><li>**size**</li></ul></li><li>**var:** <ul><li>**fstype**</li></ul><ul><li>**size**</li></ul></li><li>**home:** <ul><li>**fstype**</li></ul><ul><li>**size**</li></ul></li><li>**root:** <ul><li>**fstype**</li></ul><ul><li>**size**</li></ul></li></ul>|<ul><li>**name**</li><li>**boot:**<ul><li>**fstype:** ext2</li></ul><ul><li>**size:** 10</li></ul></li><li>**swap:**<ul><li>**fstype:** swap</li></ul><ul><li>**size:** 10</li></ul></li><li>**tmp:** <ul><li>**fstype:** ext4</li></ul><ul><li>**size:** 10</li></ul></li><li>**var:** <ul><li>**fstype:** xfs</li></ul><ul><li>**size:** 10</li></ul></li><li>**home:** <ul><li>**fstype:** ext4</li></ul><ul><li>**size:** 10</li></ul></li><li>**root:** <ul><li>**fstype:** ext4</li></ul><ul><li>**size:** 50</li></ul></li></ul>| <ul><li>**name**</li><li>**boot:** boot partition</li><li>**swap:** swap partition</li><li>**tmp:** tmp partition </li><li>**var:** var partition</li><li>**home:** home partition</li><li>**root:** root partition</li><li>**fstype:** file system type</li><li>**size:** size in percentage format</li><li>**noted:** <ul><li>**partition support:** xfs,ext2,ext3,ext4, swap for swap</li></ul><ul><li>**size:** size must be in percentage digit and total accumulation size must be 100%</li></ul></li></ul>
|hostgroup_system:<ul><li>**os**</li><li>**architecture**</li><li>**medium**</li></ul>|<ul><li>**os:** centos7</li><li>**architecture:** x86_64</li><li>**medium:** Centos7</li></ul>|<ul><li>**os:** assign operating system name(str, required)</li><li>**architecture:** assign architecture name (str, required)</li><li>**medium:** assign medium name(str, required)</li></ul>
|hostgroup:<ul><li>**name**</li><li>**subnet**</li><li>**domain**</li><li>**partition_table**</li></ul>|<ul><li>**name:** hostg_master</li><li>**subnet:** subnet1012</li><li>**domain:** example.com</li><li>**partition_table:** Kickstart default</li></ul>|<ul><li>**name:** name of hostgroup(str, required)</li><li>**subnet:** name of subnet to be assigned(str, required)</li><li>**domain:** name of domain to be assigned(str, required)</li><li>**partition_table:** name of partition table to be assigned(str, required)</li></ul>|
|primary_hosts:<lu><li>**name**</li><li>**hostgroup**</li><li>**ip**</li><li>**mac**</li></lu>|<ul><li>**name:** agent_node</li><li>**hostgroup:** hostg_master</li><li>**ip:** 10.11.12.4</li><li>**mac:** 080027d487f5</li></ul>|<ul><li>**name:** host name(str, required)</li><li>**hostgroup:** assign host group(str, required)</li><li>**ip:** valid of host ip(str, required)</li><li>**mac:** valid of mac address(str, required)</li></ul>|
|secondary_hosts:<lu><li>**ip**</li><li>**mac**</li><li>**subnet**</li><li>**primary**</li></lu>|<lu><li>**ip:** 10.11.12.6</li><li>**mac:** 080027F8D3E8</li><li>**subnet:** subnet1012</li><li>**primary:** agent_node</li></lu>|<ul><li>**ip:** ip address, must be unique(str, required)</li><li>**mac:** mac address, must be unique(str, required)</li><li>**subnet:** valid subnet to be assigned(str, required)</li><li>**primary:** valid primary node name to be assigned(str, required)</li></ul>|
|protocol: <ul><li>**type**</li></ul>|<ul><li>**type:** http</li></ul>|<ul><li>**type:** only support http(str, required)</li></ul>|
|foreman_proxy: <ul><li>**port**</li></ul>|<ul><li>**port:** 8443</li></ul>|<ul><li>**port:** port of foreman_proxy(int, required)</li></ul>|
|architecture:<ul><li>**name**</li></ul>|<ul><li>**name:** x86_64</li></ul>|<ul><li>**name:** currently only support x86_64 version</lu></ul>|
|medium:<ul><li>**name**</li><li>**path**</li><li>**os-family**</li></ul>|<ul><li>**name:** Centos7</li><li>**path:** /repos/CentOS_7_x86_64/</li><li>**os-family:** RedHat</li></ul>|<ul><li>**name:** name of os(str, required)</li><li>**path:** location of image(str, required)</li><li>**os-family:** type of os(str, required)</li></ul>|
|setting:<ul><li>**name**</li><li>**value**</ul></li>|<ul><li>**name:** token_duration</li><li>**value:** 0 </li></ul>|<ul><li>**name:** name of foreman variable setting(str, required)</li><li>**value:** value to be assigned(int/str, required)</li></ul>|
|os:<ul><li>**name**</li><li>**family**</li><li>**password-hash**</li><li>**architectures:** <ul><li>**name:**</li></ul></li><li>**provisioning-template:** <ul><li>**name:**</li></ul></li><li>**medium:** <ul><li>**name**</li></ul></li></ul>|<ul><li>**name:** centos7</li><li>**family:** RedHat</li><li>**password-hash:** SHA512</li><li>**architectures:** <ul><li>**name:** x86_64</li></ul></li><li>**provisioning-template:** <ul><li>**name:** Kickstart default</li></ul><ul><li>**name:** Kickstart default finish</li></ul><ul><li>**name:** Kickstart default PXELinux</li></ul><ul><li>**name:** Kickstart default iPXE</li></ul><ul><li>**name:** Kickstart default user data</li></ul></li><li>**medium:**<ul><li>**name:** CentOS7</li></ul>|<ul><li>**name:** name of os(str, required)</li><li>**family:** family of os(str, optional)</li><li>**password-hash:** hash password(str, optional)</li><li>**architectures:** <ul><li>**name:** name of architectures(str, optional)</li></ul></li><li>**provisioning-template:** <ul><li>**name:** name of provisioning-template(str, optional)</li></ul><ul><li>**name:** name of provisioning-template(str, optional)</li></ul><ul><li>**name:** name of provisioning-template(str, optional)</li></ul><ul><li>**name:** name of provisioning-template(str, optional)</li></ul><ul><li>**name:** name of provisioning-template(str, optional)</li></ul></li><li>**medium:** <ul><li>**name:** name of medium assigned(str, optional)</li></ul>|



## Complete YAML User Template for foreman
---------------------------------------
User is allowed to modify as they need according to requirement to do provisiong process. You may find it in /mdr_platform_bare_metal/ansible/mdr_cluster/config.yml

    foreman:

        auth:
            foreman_fqdn: bootstrap.example.com
            foreman_ip: 10.11.12.23

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
    common:

      hostgroups:
          - name: ambari
            subnet: subnet1
            domain: example.com
            partition_table: Kickstart default

          - name: ambari2
            subnet: subnet1
            domain: example.com
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


## Complete YAML System Default Template for foreman
----------------------------------------------------
It is restricted for user making changes on system.yml.j2 file below, but it is configurable and allow to be modified as per user need. There are two templates provided, CentOS7 and RedHat7 you may switch it by rename the file name as system.yml.j2 but CentOS7 will be used as default. Before proceed provisioning you may find those files in /mdr_platform_bare_metal/ansible/mdr_cluster/fmconfig/.

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



## Installation Menu for foreman
---------------------------------

| Variable      | Description  |
|:------------- |:-------------|:-----|
| Node Provision| proceed with nodes provisioning only|
| Cluster| presume nodes already exist and proceed with ambari and hdp cluster|
| Node Provision & Cluster | proceed with node provisioning and followed by ambari and hdp cluster |
| Add/Remove HDP Data nodes | adding new worker nodes and removing pre-existing worker nodes from and to hdp cluster|
| Add/Remove Elasticsearch Data nodes | adding new data nodes and removing pre-existing data nodes from and to elastic search cluster|
| Quit | Terminate the process|

## Disk partition logic for foreman provisioning
--------------------------------------------------
    Disk partition logic and configuration can be modified as below:

    partition_system(default minimum size):
    mdr_platform_bare_metal/ansible/mdr_cluster/fmconfig/system.yml.j2

    partition_table:
    mdr_platform_bare_metal/ansible/mdr_cluster/config.yml

    logic requirement:
    if  real disk size >=  disk_minimum
        set disk from patition_table
    else
        set auto default which is:
        /boot= 750 mb
        /swap=
            if memory less then 2GB
                /swap=double size of memory
            else
                /swap=memory size + 2GB
        /root= remaining size of disk

    if one of disk percentage size in partition_table < one of disk size in partition_system
       /root,/swap,/home,/var,/boot,/tmp = set base on partition_system
    else
       /root,/swap,/home,/var,/boot,/tmp =  set base on partition_table


    recommand minimum size:
        minimum size of disk is = 500 GB for each of node/host
        recommand minimum size of partition(in MB):
            boot_size=730
            swap_size=8192
            home_size=5120
            var_size=102400
            tmp_size=102400
            root_size=281138


			
			
			
## Configuration for setup pip local repository
------------------------------------------------
    - check out /mdr_platform_bare_metal/pip_repository
    - ensure you are in root user
	- extract file pypi.tar.gz(tar -xvzf pypi.tar.gz) in somewhere
	- execute file "start_pypi.sh", pypi-server and prerequisite will be installed
	- create directory for all of python packages(ex: ~/packages)
	- run pypi-server by command: nohup pypi-server -p 8008 -P . -a . ~/packages/ &
	- check ip running on localhost:8008,127.0.0.1:8008
			
## Configuration for cluster setup
---------------------------------

Following Yaml configuration template structure used for configuring the playbooks  

```
common:
    hostgroups:
        - name: name of the hostgroup
          domain: domain for the hosts in this group
          root_pass: root password for all hosts attached to this group
   primary_hosts:
      - name: name of the host excluding domain name
        hostgroup: hostgroup name to map this host mentioned in the common[hostgroups] section
        ip: ip adress of the host
        tags:   # Optional, This allows mapping single host to multiple host groups or tags within a environment, we don't allow sharing tags or hostgroups or hostnames between enviroments
           - tag name 1 # Name should be unique from hostgroup names
           - tag name 2
#It launches multiple clusters with different configurations eg: production, staging, etc. cluster1 and cluster2 are the names used for the cluster group. We can use any name to environment, in the below configuration it is cluster1, cluster2, etc.
cluster1:
    default:
        dns_enabled: yes or no to update /etc/hosts file if dns server is not available
        java_vendor: oracle or openjdk,this variable is to install java according to the vendor mentioned,if it is not mentioned then by default it takes openjdk     

    ambari:
        hostgroup: hostgroup/tag mentioned in the above common[hostgroups]
        user: ambari username
        password: ambari password
        port : ambari port
        version: ambari version number

    hdp:
      blueprint: blueprint name
      blueprint_configuration: blueprint specfic configuration
      stack: hdp_stack version
      default_password: cluster default  password
      stack_version : hdp stack full version
      utils_version: hdp utils version
      cluster_type: hdp cluster type i.e multi node or single node
      cluster_name: cluste name ex:- mdr
      #This section is to group components based on deployment needs or architecture
      component_groups :
        component_group 1 :
          - component1
          - component2
        component_group 2:
          - component3
          - component4
      host_groups:
      #This section is to map component groups to be deployed on respective host groups
            - host group 1:
                components:
                  - component_group 1
                hostgroup: configured hostgroup/tag name in the common[hostgroups] and hosts belonging to this group will be added to blueprint
                configuration: hostgroup specific configuration i.e default is empty or you can skip if you don't have any
                cardinality: cardinality of the groupi.e default =1  or
            - host group 2:
                components:
                  - component group 1
                  - component group 2
                hostgroup: configured hostgroup/tag name in the common[hostgroups]
                configuration: hostgroup specific configuration
                cardinality: ardinality of the groupi.e default =1

    hdp_test:
       hostgroup: configured hostgroup/tag name in the common[hostgroups] on that test cases will be executed make sure to all clients are installed on that hosts  
       jobtracker_host: job tracker  host
       namenode_host: name node host
       oozie_host: oozie server host

    postgres:
       hostgroup: configured hostgroup/tag name in the common[hostgroups] on this group of nodes postgres will be installed
       version: postgres version number

    activemq:
       hostgroup: configured hostgroup/tag name in the common[hostgroups] on this group of nodes activemq will be installed
       version: activemq version number

    apache:
      hostgroup: configured hostgroup/tag name in the common[hostgroups] on this group of nodes apache and tomcat server will be installed
      tomcat_version: tomcat version number

    docker:
      hostgroup: configured hostgroup/tag name in the common[hostgroups] on this group of docker registery will be installed
      version: docker version number

    es_master:
      hostgroup: configured hostgroup/tag name in the common[hostgroups] on this group of nodes elastic search master nodes will be installed
      version: elasticsearch version number
      es_config:
        network.host: network address within which es_master cluster should be available(_[networkInterface]_, _local_, _site_, _global_)
        cluster.name: es_master cluster name
        http.port: accessing port of es_master
        transport.tcp.port: transportation port of es_master
        node.data: determine whether es_master allows to store data or not
        node.master: determine whether es_master is master or not
        bootstrap.memory_lock: it tries to lock the process address space into RAM, preventing any es_master memory from being swapped out
      es_heap_size: to specify the maximum size of total heap space for es_master

    es_node:
      hostgroup: configured hostgroup/tag name in the common[hostgroups] on this group of nodes elastic search worker nodes will be installed
       es_config:
        network.host: network address within which es_node cluster should be available (_[networkInterface]_, _local_, _site_, _global_)
        cluster.name: es_node cluster name
        http.port: accessing port of es_node
        transport.tcp.port: transportation port of es_node
        node.data: determine whether es_node allows to store data or not
        node.master: determine whether es_node is master or not
        bootstrap.memory_lock: it tries to lock the process address space into RAM, preventing any es_node memory from being swapped out
      es_api_port: interaction port of es_node

    kibana:
      hostgroup: configured hostgroup/tag name in the common[hostgroups] on this group of nodes kibana will be installed
      elasticsearch_url: elasticsearch master host adddress to use
      version: kibana version number

    mongodb:
      hostgroup: configured hostgroup/tag name in the common[hostgroups] on this group of nodes mongodb will be installed
      version: mongodb version number
cluster2:
    default:
        dns_enabled: yes or no to update /etc/hosts file if dns server is not available
        java_vendor: oracle or openjdk,this variable is to install java according to the vendor mentioned,if it is not mentioned then by default it takes openjdk
    httpd:
        hostgroup: configured hostgroup/tag name in the common[hostgroups] on this group of nodes mongodb will be installed
        version: httpd version number
		lb: true/false to genereate loadbalancing configuration from the below 'config' element
		#Optional configuration for httpd load balancer; if lb is configured to true
		config:
			- balancer:
					uri: mylb1 # loadbalancer name uri eg: mybalancer
					member:
						- host1 # load balancer url http://host1:8080/app
						- host2 # load balancer url http://host2:8080/app
```

## Variable Description for cluster setup
--------------------------------------------

 Variable |mandatory/optional| example| Description
 ---------|---|----|-------
 common[hostgroups]|mandatory| |list of the host groups avaible to use by the Components
 common[hostgroups]|mandatory|[{name: master_1, subnet: subnet1, domain: example.com,  root_pass:as12345678}] |{name: name of the host group,domain: domain name of the group,root_pass: root pass of the hosts belonging to this group}
 common[primaryhosts]|mandatory|| List of hosts mapped to the hosts groups mention in the common[hostsgroups]
 common[primaryhosts]|mandatory|[{name: agent1-ambariagent,hostgroup: master_1,ip: 10.11.12.4,tags: [postgresactivemq,postgresmangodb]}]| {name: hostnmame of the machine,hostgroup: hostgroup name to which it belongs,ip: ip adress of the host,tags: list of tags to assigned to this host }
 cluster1[default][dns_enabled]|mandatory|no| flag to updated the etc hosts if dns server is not available
 cluster1[default][java_vendor]|optional|oracle|Java vendor either openjdk or oracle by default openjdk will be installed
 cluster1[ambari][hostgroup]|mandatory| master1-ambariserver.example.com| host group name or tag mentioned in the common[hostgroups] and it will be installed on the hosts of the group
 cluster1[ambari][user]|mandatory| admin| login user name of the ambari interface
 cluster1[ambari][pass]|mandatory| admin| login password of the ambari interface
 cluster1[ambari][version]|mandatory| 2.5.2.0| Ambari version number
 cluster1[hdp][blueprint]|mandatory| mdr-ha-blueprint| hdp cluster blueprint name
 cluster1[hdp][blueprint_configuration]|optional|zoo.cfg: [autopurge.purgeInterval: 24]| configurations specific here will be replaced in blue print configuration default its empty
 cluster1[hdp][stack]|mandatory|2.5| hdp stack number to be setup
 cluster1[hdp][stack_version]|mandatory|2.6.2.0| Full version of hdp including minimum version
 cluster1[hdp][utils_version]|mandatory|1.1.10.21| Full Hdp utils version
 cluster1[hdp][cluster_type]|mandatory|multi_node|Hdp cluster type to be formed it must be either multi_node or single_node in case of single node all compnents listed in component groups added to blueprint
 cluster1[hdp][component_groups]|mandatory|hive_components,[HIVE_METASTORE,HIVE_SERVER,HCAT,WEBHCAT_SERVER,HIVE_CLIENT,MYSQL_SERVER]| Component Groups is group of key as group name and array of values with the components. and this can be used in any where in any host_groups[components]. Group name based on user preference
 cluster1[hdp][component_groups][component_group_name][components]|mandatory|hive_components| Array of the components of that group
 cluster1[hdp][host_groups]|mandatory||host groups specification and its configuration mentioned here added to the blue print
 cluster1[hdp][host_group_name][components]|mandatory|hive_components|List of the component groups mentioned in hdp[component_groups] to be added to blue print and for single node it has not effect
 cluster1[hdp][host_groups][host_group_name][hostgroup]|mandatory|master_1| host group or tag configured in common[hostgroups] and hosts will beloning to this group will be added to this host group in blueprint
 cluster1[hdp][host_groups][host_group_name][configuration]|optional|| Configurations mentioned here will be applied to hostgroup specific configuration in the blueprint
 cluster1[hdp][host_groups][hosts_group_name][cardinality]|optional|1| cardinality of the host group to be added in blueprint default is 1
 cluster1[hdp_test][hostgroup]|mandatory|edge_1| hostgroup name or tag configured in common[hostgroups] to run hdp test cases and make sure to have all required clients istalled in that hosts
 cluster1[hdp_test][jobtracker_host]|mandatory|agent8-ambariagent.example.com|Job tracker host to be used by test case job
 cluster1[hdp_test][namenode_host]|mandatory|agent1-ambariagent.example.com| Namenode host to be used by test case job
 cluster1[hdp_test][oozie_host]|mandatory|agent10-ambariagent.example.com|oozie server host to be used by test case job
 cluster1[postgres][hostgroup]| mandatory|postgress| hostgroup name or tag configured in common[hostgroups] to install postgres  and on this group of hosts postgres will be installed
 cluster1[postgres][version]| mandatory|9.6| postgres version number
 cluster1[activemq][hostgroup]| mandatory|activemq| hostgroup name or tag configured in common[hostgroups] to install activemq  and on this group of hosts activemq will be installed
 cluster1[activemq][version]| mandatory|5.15.0| activemq version number
 cluster1[es_master][hostgroup]|mandatory|es_master| hostgroup name or tag configured in common[hostgroups] to install elastic search  and on this group of hosts elastic search masters will be installed
 cluster1[es_master][version]| mandatory|5.5.0| elasticsearch version number
 cluster1[es_master][es_config][network.host]| mandatory|_site_|_[networkInterface]_: Addresses of a network interface, for example _en0_, _local_: Any loopback addresses on the system, for example 127.0.0.1, _site_: Any site-local addresses on the system, for example 192.168.0.1, _global_: Any globally-scoped addresses on the system, for example 8.8.8.8.
 cluster1[es_master][es_config][cluster.name]| mandatory|es-cluster|es_master cluster name
 cluster1[es_master][es_config][http.port]| mandatory|9200| accessing port of es_master
 cluster1[es_master][es_config][transport.tcp.port]| mandatory|9300| transportation port of es_master
  cluster1[es_master][es_config][node.data]| mandatory|true| determine whether es_master allows to store data or not
 cluster1[es_master][es_config][node.master]| mandatory|true|determine whether es_master is master or not
 cluster1[es_master][es_config][bootstrap.memory_lock]| mandatory|false| it tries to lock the process address space into RAM, preventing any es_master memory from being swapped out
 cluster1[es_master][es_heap_size]| mandatory|1g| to specify the maximum size of total heap space for es_master
 cluster1[es_node][hostgroup]| mandatory|es_node| hostgroup name or tag configured in common[hostgroups] to install elastic search worker nodes and on this group of hosts elastic search nodes will be installed
 cluster1[es_node][es_config][network.host]| mandatory|_site_|_[networkInterface]_: Addresses of a network interface, for example _en0_, _local_: Any loopback addresses on the system, for example 127.0.0.1, _site_: Any site-local addresses on the system, for example 192.168.0.1, _global_: Any globally-scoped addresses on the system, for example 8.8.8.8.
 cluster1[es_node][es_config][cluster.name]| mandatory|es-cluster|es_node cluster name
 cluster1[es_node][es_config][http.port]| mandatory|9200| accessing port of es_node
 cluster1[es_node][es_config][transport.tcp.port]| mandatory|9300| transportation port of es_node
  cluster1[es_node][es_config][node.data]| mandatory|true| determine whether es_node allows to store data or not
 cluster1[es_node][es_config][node.master]| mandatory|false|determine whether es_node is master or not
 cluster1[es_node][es_config][bootstrap.memory_lock]| mandatory|false| it tries to lock the process address space into RAM, preventing any es_node memory from being swapped out
 cluster1[es_node][es_api_port]| mandatory|9200| interaction port of es_node
 cluster1[kibana][hostgroup]| mandatory|kibana| hostgroup name or tag  configured/availble in common[hostgroups] to install kibana and on this group of hosts kibana will be installed
 cluster1[kibana][elasticsearch_url]|mandatory|http://master1-ambariserver.example.com:9200 | Elastic search url to be used by the kibana
 cluster1[kibana][version]| mandatory|5.5.0| kibana version number
 cluster1[apache][hostgroup]| mandatory| apache|hostgroup name or tag configured in common[hostgroups] to install apache and tomcat and on this group of hosts tomcat and apache will be installed
 cluster1[apache][tomcat_version]| mandatory|7.0.76| tomcat version number
 cluster1[httpd][hostgroup]| mandatory| httpd|hostgroup name or tag configured in common[hostgroups] to install httpd on this group of hosts apache httpd will be installed
 cluster1[httpd][version]| mandatory|2.4.6| httpd version number
 cluster1[httpd][lb]| mandatory|true/false| load balnacer to be created on web server
 cluster1[httpd][config]| mandatory|balancer1| load balancer configuration
 cluster1[httpd][config][balancer][uri]| mandatory|mybalancer| uri name for the loadbalancer
 cluster1[httpd][config][balancer][member]| mandatory|http://host:8080/app| url of the application
 cluster1[docker][hostgroup]|mandatory|docker|hostgroup name or tag configured in common[hostgroups] to install docker and on this group of hosts docker will be installed
 cluster1[docker][version]| mandatory|17.09.0| docker version number

## Default configuration template for foreman and cluster setup
---------------------------------------------------------------
 Please refer to default template
 https://engineering/bitbucket/projects/TA/repos/mdr_platform_bare_metal/browse/ansible/mdr_cluster/config.yml

## Add/Remove nodes from HDP cluster
---------------------------------------------------------------
  Datanodes can be added/removed with option 4 and currently supports the nodes which has components DATANODE,NODEMANAGER and METRICS_MONITOR.First New nodes will be added and then existing nodes will be removed if any configured.Please refer to default template https://engineering/bitbucket/projects/TA/repos/mdr_platform_bare_metal/browse/ansible/mdr_cluster/update_hdp_cluster.yml

### Adding Datanodes to HDP cluster
---------------------------------------------------------------
 Configured nodes will be added to the hdp host group mentioned and only remommeded is Datanodes


### Removing Datanodes from HDP cluster
---------------------------------------------------------------
 Datanodes can be removed from the hdp cluster by configuring in list of datanodes needs to be removed section and Cluster must have one data node

### Configuration for Add/Remove HDP cluster
---------------------------------------------------------------
 ```
 default:
   java_vendor: Java vendor to be installed on ambari agent either oracle or openjdk
   dns_enabled: yes or no to update cluster nodes /etc/host file if dns server not available

 ambari:
    host : Hostname of the ambari
    port : Port number of the ambari
    user: Ambari username
    password: Ambari Password
    version: Ambari Version

 hdp:
   clustername: CluserName ex : mdr
   blueprint: blueprint name
   add:
     hosts:
        - name: hostnmae of the new node 1 to be added
          ip: ip address of the node 1
        - name: hostnmae of the new node 2 to be added
          ip: ip adress of node 2
     hostgroup: hdp hostgroup name to attach the nodes in hosts section
   remove:
      hosts:
        - name: Hostname of the node to be removed
 ```

### Example of default Template for Add/Remove HDP cluster
---------------------------------------------------------------
  Please refer to default template
  https://engineering/bitbucket/projects/TA/repos/mdr_platform_bare_metal/browse/ansible/mdr_cluster/update_hdp_cluster.yml

### Variable Description for Add/Remove HDP cluster
---------------------------------------------------------------
 Variable |mandatory/optional| example| Description
 ---------|---|----|-------
  default[java_vendor]|optional|oracle| Java/jdk vendor to be installed on New data nodes default is opendk, Only supported oracle or openjdk
  default[dns_enabled]|mandatory|no| yes or no, To update the etc/host files in all the nodes of cluster if we dont have dns server in network
  ambari[host]|mandatory|master1-ambariserver.example.com| Ambari host name for Sumbiting to node adding/deleting requests
  ambari[port]|mandatory|8080| Port Number of the ambari
  ambari[version]|mandatory|2.5.2.0| Ambari version number to setupo the ambari agent on the newly added Datanodes
  hdp[clustername]|mandatory|mdr| configured clusternmae during inital lauch of cluster
  hdp[bluerprintn]|mandatory|mdr-ha-blueprint| blueprint name used for deploying the hdp cluster during intial lauch of cluster
  hdp[add]|optional|| config subsection for Newly adding hosts and its optional if you dont need to add Datanodes
  hdp[add][hosts]|optional| Newly adding hosts configuration section and its optional if you dont need to add Datanodes
  hdp[add][hosts]|optional|{name: mandatory,ip: optional}| Yaml array of hosts with optional ip adress those needs to be added to Datanodes hostgroup
  hdp[add][hostgroup]|mandatory in case if you need to add hosts| exisitng hostgroup name in the cluster to assign the hosts in the host specification
  hdp[remove]|optional||config subsection for datanodes to be removed
  hdp[remove][hosts]|optional|[{name:agent7-ambariagent.example.com}]| Hostnames of the datanodes to be removed


### Example of default Template for Add/Remove HDP cluster
  ---------------------------------------------------------------
  Please refer to default template
  https://engineering/bitbucket/projects/TA/repos/mdr_platform_bare_metal/browse/ansible/mdr_cluster/update_hdp_cluster.yml

---------------------------------------------------------------


## Adding or Removing Elastic Search Data Nodes

  Elastic search datanodes can be added or removed from the option 5 in the bootstrap menu, as of now,we only supports the adding new data nodes and decommissioning existing data nodes in the cluster.
       Note: in case of removing nodes we only decommissioning the nodes with elastic search api, after finishing the ansible execution user needs to decide  if all the data in the node has rebalanced within the cluster then user can shutdown the intended nodes and decommissioning only based on host name of the node

### Configuration template for adding/removing datanodes

---------------------------------------------------------------
 ```
 default:
   java_vendor: Java vendor to be installed on new nodes  oracle or openjdk
   dns_enabled: yes or no to update cluster nodes /etc/hosts file if dns server not available

 es_master:
    host : Hostname of the elasticsearch master
    version: Version number of elastic search to setup
    es_heap_size: JVM heap size of the newly added data nodes
 es_node:
   add:
     hosts:
        - name: hostnmae of the new node 1 to be added
          ip: ip address of the node 1
        - name: hostnmae of the new node 2 to be added
          ip: ip adress of node 2
     hostgroup: hdp hostgroup name to attach the nodes in hosts section
   remove:
      hosts:
        - name: Hostname of the node to be removed
   es_config: # Configuration parameters to place in elasticsearch.yml some of the mandatories we have defiend here and user can add any additional
        network.host:  Network host parameter in elasticsearch.yml file
        cluster.name: Existing elasticsearch clustername to add new nodes
        http.port: Http Api port number to be used by new nodes
        transport.tcp.port: TCP port number to be used by new nodes
        node.data: New nodes supports data or not
        node.master: New nodes are master or data node. note: we only support data nodes
        bootstrap.memory_lock: Elastic search RAM memory lock to avoid swapping
    es_api_port: HTTP rest api port number on the newly added data nodes


 ```


### Example of default Template for Add/Remove Elastic search data nodes

  Please refer to the default template [update_es_cluster.yml](https://engineering/bitbucket/projects/TA/repos/mdr_platform_bare_metal/browse/ansible/mdr_cluster/update_es_cluster.yml)

### Variable Description for Add/Remove Elastic search Data nodes
  ---------------------------------------------------------------
   Variable |mandatory/optional| example| Description
    ---------|---|----|-------
    default[java_vendor]|optional|oracle| Java/jdk vendor to be installed on New data nodes default is openjdk, Only supported oracle or openjdk
    default[dns_enabled]|mandatory|no| yes or no, To update the etc/host files in all the nodes of cluster if we dont have dns server in network
    es_master[host]|mandatory|agent3-ambariagent.example.com| Elastic search master host name for submittng to node adding/deleting requests
    es_master[version]|mandatory|5.5.0| Elastic search version number to setup the new data nodes
    es_master[es_heap_size]|mandatory|1g| JVM heap size of the newly added data nodes
    es_node[es_config][network.host]|mandatory|_site_|_[networkInterface]_: Addresses of a network interface, for example _en0_, _local_: Any loopback addresses on the system, for example 127.0.0.1, _site_: Any site-local addresse on the system, for example 192.168.0.1, _global_: Any globally-scoped addresses on the system, for example 8.8.8.8.  
    es_node[es_config][cluster.name]|mandatory|es-cluster| configured elastic search clustername during initial launch of cluster
    es_node[es_config][http.port]|mandatory|9200|  http rest api port number of newly added data nodes
    es_node[es_config][transport.tcp.port]|mandatory|9300| Tcp port number of the newly added data nodes
    es_node[es_config][node.data]|mandatory|true| true if newly added data nodes supports storing data on it,false if no
    es_node[es_config][node.master]|mandatory|false|true if newly added nodes acts as a master nodes, false if no
    es_node[es_config][bootstrap.memory_lock]|mandatory|true| RAM memory to lock to avoid the swapping on node    
    es_node[add]|optional|| Config subsection for Newly adding hosts and its optional if you don't need to add Datanodes
    es_node[add][hosts]|optional| Newly adding hosts configuration section and its optional if you don't need to add Datanodes
    es_node[add][hosts]|optional|{name: mandatory,ip: optional}| Yaml array of hosts with optional ip adress those needs to be added to Datanodes hostgroup
    es_node[remove]|optional||Config subsection for datanodes to be removed
    es_node[remove][hosts]|optional|[{name:agent7-ambariagent.example.com}]| Hostnames of the datanodes to be removed

## Service ports in general
---------------------------------------------------------------
### Hadoop Components
Service | Port number
--------|------------
App TimeLine Server Interface| 8188
Job History Service Interface|19888
NameNode WebUI|50070
DataNode WebUI|50075
Resource Manager|8025
Hive Web Ui|9999
Hive Metastore|9083
Mysql Server|3306
Oozie Jobs Interface|11000

For additional default ports information can be found at [hortonworks website](https://docs.hortonworks.com/HDPDocuments/HDP2/HDP-2.6.2/bk_reference/content/reference_chap2.html)
### Non Hadoop components
Service | Port number
--------|------------
activemq|61616
postgres|5432
elasticsearch api|9200
kibana webinterface|5601
docker|5000
tomcat|8080
httpd|80
mongodb|27017
foreman proxy|8443

## Authentication menu in general
---------------------------------
    Enter Foreman Authentication
    Username: foreman_username
    Password: foreman_password
    Password (again): confirm foreman_password

    Enter HDP Password
    Password: hdp_passport
    Password (again): confirm hdp_passport

	Enter Nodes Password to be set while foreman provisioning
    Password: node_passport
    Password (again): confirm node_passport

    Enter Nodes Username and Password for cluster launch
    Minimum 8 characters required
    Username: node_user
    Password: node_password

## Foreman URL and ambari server
--------------------------------
    web interface can be accessed through:
    foreman:
        http://bootstrap.example.com/users/login
        default authentication:
        username = 'admin'
        password = 'input password'

    ambari server:
        http://master1-ambariserver.example.com:8080
        default authentication:
        username = 'admin'
        password = 'admin'

    note:check your particular host name for bootstrap and ambari server

## Origin Repo
 https://engineering/bitbucket/projects/TA/repos/mdr_platform_bare_metal

## HDP Blueprints (This section contains blueprint design specification and architecture documentation)
 https://engineering/bitbucket/projects/TA/repos/mdr_platform_bare_metal/browse/blueprints
 https://engineering/confluence/display/MSS/Ambari+Blueprint+Design+Specification

Software Versions
-----------------
| Software       | Version        |
| :------------- | :------------- |
| ActiveMQ       |     5.15       |
| Ambari         |     2.5.2      |
| Ansible        |     2.3.1.0    |
| Apache  Tomcat |     7.0.76     |
| CentOS         |     7.1        |
| Elastic Search |     5.5.0      |
| Foreman        |     1.15.13    |
| HDP            |     2.5 & 2.6  |
| Java SE        |     1.8        |
| Kibana         |     5.5.0      |
| Mongo          |     3.4.10     |
| MySql          |     5.6.38-2   |
| Postgres       |     9.6        |
| Python         |     2.7        |
| Python-pip     |     8.1.2      |


## Prerequisite
---------------

    1. Bootstrap machine
          - support centos 7
          - gnome UI must be installed
          - at least 20 GB hardisk and 2 GB ram
          - log in as a root user

    2. Setup SE Linux permissive or disabled
          - modified: /etc/sysconfig/selinux
          - restart machine

    3. Setup firewall or disable it
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

	  4. Install local yum and pypi Repository setup on bootstrap machine

          - installation of Nginx Repository
	              https://engineering/bitbucket/projects/TA/repos/mdr_platform_bare_metal/browse/nginx

          - installation of pypi
                * pypi should be installed in sameplace where http repository was installed.
                * install pip:
                      yum -y install python-pip
                * install pypi server:
                      pip install pypiserver
                * download packages.tar.gz :
                      wget -N http://10.129.6.237/repos/zip_repo/packages.tar.gz
                * unzip file:
                      tar xvfz packages.tar.gz ~/
                * run command:
                      nohup pypi-server -p 8008 -P . -a . ~/packages/ &
                * verify by using curl or open browser:
                      http://repo_url:8008/packages
                * pypi local repository must be bind using port 8008.

    5. If DNS required, Making sure your DNS address is resolveable
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

    6. Making sure that you don't have any DHCP server available which is been connecting to the subnet network

    7. Making sure that your network device interface or network interface in bootstrap machine e.g; "eth0" is
       dedicated only for single Ip

    8. Make sure your http_proxy and https_proxy is disabled, check as well in /etc/yum.conf

    9. If you have existing Ansible, Required Ansible version : ansible 2.3.1.0

    10. The best approach is for having static Ip for bootstrap machine, check how to setup static Ip below:

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


## Quickstart in general
---------------------------------------------------------------
Following are the steps to be done for provisioning the nodes and to setup cluster

```
git clone ssh://git@10.37.0.35:7999/ta/mdr_platform_bare_metal.git
* cd /mdr_platform_bare_metal/ansible/mdr_cluster
* configure:
      config.yml:
      	- /mdr_platform_bare_metal/ansible/mdr_cluster/config.yml

* launch:
      - cd /mdr_platform_bare_metal/ansible/mdr_cluster/
      - ./bootstrap.sh http://<repo_url> ,example as below
	    ./bootstrap.sh http://10.129.6.237

    while running this scirpt it will prompt for options as below
    1. Node Provision
    2. Node Provision & Cluster
    3. Cluster
    4. Add/Remove HDP Data nodes
    5. Add/Remove Elasticsearch Data nodes
    6. Quit

   below are the description for each option
   1) Node provisioning: This does only the provisioning task which is basic software installation in a bare metal machine giving with MAC address. By triggering this option it installs the ansible and foreman in bootstrap machine and thereby foreman provisions the nodes supplied by the MAC address which has be mentioned in config.yml as highlighted before.
   2) Cluster: This skips the installation of foreman and installs only ansible in bootstrap machine ,thereby ansible takes care of  triggering the installation of software  which has been mentioned in config.yml to the target nodes
   3) Node provisioning & Cluster: This does foreman provisioning followed by cluster setup on those machines which has been provisioned by foreman.
   4) Add/Remove HDP Data nodes: This allows to add/remove the data nodes from HDP cluster
   5) Add/Remove Elasticsearch Data nodes: This allows to add/remove data nodes form elasticsearch cluster
   6) Quit: Terminate the process

```
This will automatically update the required configurations for ansible roles and executes playbooks which setups the hdp cluster and remaining packages

note:While choosing Node provisioning option, you see provisioning is ready you might turn up the nodes to be provisioned,from bios setting you may choose boot from network and allow boot using PXELinux. After the installation You may find the rest of log in /var/log/ansible.log

## Licence
-----------
Mdr_Platform_bare_metal - Copyright (c) 2017 BAE Systems Applied Intelligence.
