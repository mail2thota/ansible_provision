# Project:
mdr_platform_bare_metal
## Synopsis:
Ansible package/playbooks for setting up ambari,hdp cluster,tomcat,docker registery,postgres database,mongodb and activemq

## Motivation:
To abstrct complexity of provising hdp cluster usig ansible playbooks.

## Origin Repo:
https://engineering/bitbucket/projects/TA/repos/mdr_platform_bare_metal/browse/ansible/mdr_cluster/bootstrap.sh


## Quickstart:
Assuming that the nodes are provisioned with OS and dependencies using foreman  or manually,thereby run below command

```
git clone ssh://git@10.37.0.35:7999/ta/mdr_platform_bare_metal.git
* cd /mdr_platform_bare_metal/ansible/mdr_cluster
* configure:
      config.yml:
      	- /mdr_platform_bare_metal/ansible/mdr_cluster/config.yml

* launch:
      - cd /mdr_platform_bare_metal/ansible/mdr_cluster/
      - ./bootstrap.sh http://repository_ip

when script prompt you choose the appropriate option

```
This will automatically updates the required configurations for ansible roles and executes playbooks which setups the hdp cluster and remaining packages

## Configuration:

Following Yaml configuration template structure used for configuring the playbooks  

```
---


default:
    dns_enabled: yes or no to update /etc/hosts file if dns server is not available
    java_vendor: oracle or openjdk,this variable is to install java according to the vendor mentioned,if it is not mentioned then by default it takes openjdk     

common:
    hostgroups:
        - name: name of the hostgroup
          domain: domain for the hosts in this group
          root_pass: root password for all hosts attached to this group
   primary_hosts:
      - name: name of the host excluding domain name
        hostgroup: hostgroup name to map this host mentioned in the common[hostgroups] section
        ip: ip adress of the host

ambari:
    hostgroup: hostgroup mentioned in the above common[hostgroups]
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
  component_groups :
    component_group 1 :
      - component1
      - component2
    component_group 2:
      - component3
      - component4
  host_groups:
        - host group 1:
            components:
              - component_group 1
            hostgroup: configured hostgroup name in the common[hostgroups] and hosts belonging to this group will be added to blueprint
            configuration: hostgroup specific configuration i.e default is empty or you can skip if you don't have any
            cardinality: cardinality of the groupi.e default =1  or
        - host group 2:
            components:
              - component group 1
              - component group 2
            hostgroup: configured hostgroup name in the common[hostgroups]
            configuration: hostgroup specific configuration
            cardinality: ardinality of the groupi.e default =1

hdp_test:
   hostgroup: configured hostgroup name in the common[hostgroups] on that test cases will be executed make sure to all clients are installed on that hosts  
   jobtracker_host: job tracker  host
   namenode_host: name node host
   oozie_host: oozie server host

postgres:
   hostgroup: configured hostgroup name in the common[hostgroups] on this group of nodes postgres will be installed
activemq:
   hostgroup: configured hostgroup name in the common[hostgroups] on this group of nodes activemq will be installed

apache-server:
  hostgroup: configured hostgroup name in the common[hostgroups] on this group of nodes apache and tomcat server will be installed

docker-registry:
  hostgroup: configured hostgroup name in the common[hostgroups] on this group of docker registery will be installed

es_master:
  hostgroup: configured hostgroup name in the common[hostgroups] on this group of nodes elastic search master nodes will be installed

es_node:
  hostgroup: configured hostgroup name in the common[hostgroups] on this group of nodes elastic search worker nodes will be installed

kibana:
  hostgroup: configured hostgroup name in the common[hostgroups] on this group of nodes kibana will be installed
  elasticsearch_url: elasticsearch master host adddress to use

mongodb:
  hostgroup: configured hostgroup name in the common[hostgroups] on this group of nodes mongodb will be installed
```
Please refer to the existing default template[config file](https://engineering/bitbucket/projects/TA/repos/mdr_platform_bare_metal/browse/ansible/mdr_cluster/config.yml)
## Variables Description
 Variable |mandatory/optional| example| Description
 ---------|-|--------|-------
 default[dns_enabled]|mandatory|no| flag to updated the etc hosts if dns server is not available
 default[java_vendor]|optional|oracle|Java vendor either openjdk or oracle by default openjdk will be installed
common[hostgroups]|mandatory| |list of the host groups avaible to use by the Components
common[hostgroups]|mandatory|[{name: master_1, subnet: subnet1, domain: example.com,  root_pass:as12345678}] |{name: name of the host group,domain: domain name of the group,root_pass: root pass of the hosts belonging to this group}
common[primaryhosts]|mandatory|| List of hosts mapped to the hosts groups mention in the common[hostsgroups]
common[primaryhosts]|mandatory|[{name: agent1-ambariagent,hostgroup: master_1,ip: 10.11.12.4}]| {name: hostnmame of the machine,hostgroup: hostgroup name to which it belongs,ip: ip adress of the host }
 ambari[hostgroup]|mandatory| master1-ambariserver.example.com| host group name mentioned in the common[hostgroups] and it will be installed on the hosts of the group
 ambari[user]|mandatory| admin| login user name of the ambari interface
 ambari[pass]|mandatory| admin| login password of the ambari interface
 ambari[version]|mandatory| 2.5.2.0| Ambari version number
 hdp[blueprint]|mandatory| mdr-ha-blueprint| hdp cluster blueprint name
 hdp[blueprint_configuration]|optional|zoo.cfg: [autopurge.purgeInterval: 24]| configurations specific here will be replaced in blue print configuration default its empty
 hdp[stack]|mandatory|2.5| hdp stack number to be setup
 hdp[stack_version]|mandatory|2.6.2.0| Full version of hdp including minimum version
 hdp[utils_version]|mandatory|1.1.10.21| Full Hdp utils version
 hdp[cluster_type]|mandatory|multi_node|Hdp cluster type to be formed it must be either multi_node or single_node in case of single node all compnents listed in component groups added to blueprint
 hdp[component_groups]|mandatory|hive_components,[HIVE_METASTORE,HIVE_SERVER,HCAT,WEBHCAT_SERVER,HIVE_CLIENT,MYSQL_SERVER]| Component Groups is group of key as group name and array of values with the components. and this can be used in any where in any host_groups[components]. Group name based on user preference
 hdp[component_groups][component_group_name][components]|mandatory|hive_components| Array of the components of that group
 hdp[host_groups]|mandatory||host groups specification and its configuration mentioned here added to the blue print
 hdp[host_group_name][components]|mandatory|hive_components|List of the component groups mentioned in hdp[component_groups] to be added to blue print and for single node it has not effect
 hdp[host_groups][host_group_name][hostgroup]|mandatory|master_1| host group configured in common[hostgroups] and hosts will beloning to this group will be added to this host group in blueprint
 hdp[host_groups][host_group_name][configuration]|optional|| Configurations mentioned here will be applied to hostgroup specific configuration in the blueprint
 hdp[host_groups][hosts_group_name][cardinality]|optional|1| cardinality of the host group to be added in blueprint default is 1
 hdp_test[hostgroup]|mandatory|edge_1| hostgroup name configured in common[hostgroups] to run hdp test cases and make sure to have all required clients istalled in that hosts
 hdp_test[jobtracker_host]|mandatory|agent8-ambariagent.example.com|Job tracker host to be used by test case job
 hdp_test[namenode_host]|mandatory|agent1-ambariagent.example.com| Namenode host to be used by test case job
 hdp_test[oozie_host]|mandatory|agent10-ambariagent.example.com|oozie server host to be used by test case job
 postgres[hostgroup]| mandatory|postgress| hostgroup name configured in common[hostgroups] to install postgres  and on this group of hosts postgres will be installed
 activemq[hostgroup]| mandatory|activemq| hostgroup name configured in common[hostgroups] to install activemq  and on this group of hosts activemq will be installed
 es_master[hostgroup]|mandatory|es_master| hostgroup name configured in common[hostgroups] to install elastic search  and on this group of hosts elastic search masters will be installed
 es_node[hostgroup]| mandatory|es_node| hostgroup name configured in common[hostgroups] to install elastic search worker nodes and on this group of hosts elastic search nodes will be installed
 kibana[hostgroup]| mandatory|kibana| hostgroup name configured/availble in common[hostgroups] to install kibana and on this group of hosts kibana will be installed
 kibana[elasticsearch_url]|mandatory|http://master1-ambariserver.example.com:9200 | Elastic search url to be used by the kibana
 apache-server[hostgroup]| mandatory| apache|hostgroup name configured in common[hostgroups] to install apache and tomcat and on this group of hosts tomcat and apache will be installed
 docker-registry[hostgroup]|mandatory|docker|hostgroup name configured in common[hostgroups] to install docker-registery and on this group of hosts docker-register will be installed


 Please refer below example tempate and the existing   [config template ](https://engineering/bitbucket/projects/TA/repos/mdr_platform_bare_metal/browse/ansible/mdr_cluster/roles/pre-config/config.yml) in code base if needed

 ```
 ---


default:
  dns_enabled: no
  java_vendor: oracle


common:
    hostgroups:
        - name: master_1
          subnet: subnet1
          domain: example.com
          root_pass: as12345678
          partition_table: Kickstart default
        - name: master_2
          subnet: subnet1
          domain: example.com
          root_pass: as12345678
          partition_table: Kickstart default
        - name: master_3
          subnet: subnet1
          domain: example.com
          root_pass: as12345678
          partition_table: Kickstart default
        - name: master_4
          subnet: subnet1
          domain: example.com
          root_pass: as12345678
          partition_table: Kickstart default
        - name: zk_1
          subnet: subnet1
          domain: example.com
          root_pass: as12345678
          partition_table: Kickstart default
        - name: edge_1
          subnet: subnet1
          domain: example.com
          root_pass: as12345678
          partition_table: Kickstart default
        - name: edge_3
          subnet: subnet1
          domain: example.com
          root_pass: as12345678
          partition_table: Kickstart default
        - name: worker_1
          subnet: subnet1
          domain: example.com
          root_pass: as12345678
          partition_table: Kickstart default
        - name: postgres
          subnet: subnet1
          domain: example.com
          root_pass: as12345678
          partition_table: Kickstart default
        - name: activemq
          subnet: subnet1
          domain: example.com
          root_pass: as12345678
          partition_table: Kickstart default
        - name: kibana
          subnet: subnet1
          domain: example.com
          root_pass: as12345678
          partition_table: Kickstart default
        - name: es_master
          subnet: subnet1
          domain: example.com
          root_pass: as12345678
          partition_table: Kickstart default
        - name: es_node
          subnet: subnet1
          domain: example.com
          root_pass: as12345678
          partition_table: Kickstart default
        - name: apache-server
          subnet: subnet1
          domain: example.com
          root_pass: as12345678
          partition_table: Kickstart default
        - name: mongodb
          subnet: subnet1
          domain: example.com
          root_pass: as12345678
          partition_table: Kickstart default
        - name: docker-registery
          subnet: subnet1
          domain: example.com
          root_pass: as12345678
          partition_table: Kickstart default

    primary_hosts:

        - name: agent1-ambariagent
          hostgroup: master_1
          ip: 10.11.12.4
          mac: 0800271AD0DA
        - name: agent2-ambariagent
          hostgroup: master_2
          ip: 10.11.12.5
          mac: 080027626A0D
        - name: agent3-ambariagent
          hostgroup: master_3
          ip: 10.11.12.6
          mac: 080027FE1A42
        - name: agent4-ambariagent
          hostgroup: master_4
          ip: 10.11.12.7
          mac: 08002708D5C2
        - name: agent5-ambariagent
          hostgroup: zk_1
          ip: 10.11.12.8
          mac: 080027DF8EE5
        - name: agent6-ambariagent
          hostgroup: zk_1
          ip: 10.11.12.9
          mac: 0800278B2194
        - name: agent7-ambariagent
          hostgroup: worker_1
          ip: 10.11.12.10
          mac: 08002728805D
        - name: agent8-ambariagent
          hostgroup: edge_3
          ip: 10.11.12.11
          mac: 08002743CB9C
        - name: agent9-ambariagent
          hostgroup: postgres
          ip: 10.11.12.12
          mac: 080027A55547
        - name: agent10-ambariagent
          hostgroup: activemq
          ip: 10.11.12.13
          mac: 080027D25FEE
        - name: agent11-ambariagent
          hostgroup: apache-server
          ip: 10.11.12.14
          mac: 080027EE643F
        - name: agent12-ambariagent
          hostgroup: docker-registery
          ip: 10.11.12.15
          mac: 0800275F8125
        - name: agent13-ambariagent
          hostgroup: es_node
          ip: 10.11.12.16
          mac: 080027ED84FE
        - name: agent14-ambariagent
          hostgroup: es_node
          ip: 10.11.12.17
          mac: 0800272F3847
        - name: agent15-ambariagent
          hostgroup: mongodb
          ip: 10.11.12.18
          mac: 080027A5EAB2
        - name: master1-ambariserver
          hostgroup: edge_1
          ip: 10.11.12.24
          mac: 080027BB1483  

ambari:
  hostgroup: edge_1
  user: admin
  password: admin
  port : 8080
  version: 2.5.2.0

hdp:
  blueprint: mdr-ha-blueprint
  blueprint_configuration:
  stack: 2.6
  default_password: admin
  stack_version : 2.6.2.0
  utils_version: 1.1.0.21
  cluster_type: multi_node
  cluster_name: mdr
  component_groups :
    master_1 :
      - JOURNALNODE
      - NAMENODE
      - HISTORYSERVER
      - METRICS_MONITOR
    master_2:
      - JOURNALNODE
      - APP_TIMELINE_SERVER
      - RESOURCEMANAGER
      - SPARK_JOBHISTORYSERVER
      - METRICS_MONITOR
    master_3:
      - SECONDARY_NAMENODE
      - HCAT
      - HIVE_METASTORE
      - HIVE_SERVER
      - HIVE_CLIENT
      - WEBHCAT_SERVER
      - MYSQL_SERVER
      - METRICS_MONITOR
    master_4:
      - OOZIE_SERVER
      - METRICS_MONITOR
    zk_1:
      - METRICS_MONITOR
      - ZOOKEEPER_SERVER
    edge_1:
      - METRICS_MONITOR
      - METRICS_COLLECTOR
    edge_3:
      - ZOOKEEPER_CLIENT
      - TEZ_CLIENT
      - SPARK_CLIENT
      - MAPREDUCE2_CLIENT
      - YARN_CLIENT
      - HDFS_CLIENT
      - OOZIE_CLIENT
      - HIVE_CLIENT
      - PIG
      - METRICS_MONITOR
    worker_1:
      - NODEMANAGER
      - DATANODE
      - METRICS_MONITOR
  hostgroups:
    - master_1:
        components:
          - master_1
        hostgroup: master_1
    - master_2:
        components:
          - master_2
        hostgroup: master_2
    - master_3:
        components:
          - master_3
        hostgroup: master_3
    - master_4:
        components:
          - master_4
        hostgroup: master_4
    - zk_1:
        components:
          - zk_1
        hostgroup: zk_1
        cardinality: 3
    - edge_1:
        components:
           - edge_1
        hostgroup: edge_1
    - edge_3:
        components:
          - edge_3
        hostgroup: edge_3
    - worker_1:
        components:
          - worker_1
        hostgroup: worker_1


postgres:
  hostgroup: postgres

activemq:
  hostgroup: activemq

kibana:
  hostgroup: master_3
  elasticsearch_url: http://master1-ambariserver.example.com:9200/

es_master:
  hostgroup: master_3

es_node:
  hostgroup: es_node

apache-server:
  hostgroup: apache-server

mongodb:
  hostgroup: mongodb

docker-registry:
  hostgroup: docker-registery

hdp_test:
   hostgroup: edge_3
   jobtracker_host: agent2-ambariagent.example.com
   namenode_host: agent1-ambariagent.example.com
   oozie_host: agent4-ambariagent.example.com

 ```

## Service ports
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
docker-registry|5000
tomcat|8080
httpd|80
mongodb| 27017


## Licence:
mdr_platform_bare_metal - ansible - Copyright (c) 2016 BAE Systems Applied Intelligence.
