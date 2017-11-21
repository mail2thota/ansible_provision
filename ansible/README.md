# Project:
mdr_platform_bare_metal - ambari-hdp

## Synopsis:
Ansible package/playbooks for setting up ambari,hdp cluster,postgres database and activemq

## Motivation:
To abstrct complexity of provising hdp cluster usig ansible playbooks.

## Origin Repo:
https://engineering/bitbucket/projects/TA/repos/mdr_platform_bare_metal/browse/ansible/ansible_boot.sh


## Quickstart:
Assuming that the nodes are provisioned with OS and dependencies using foreman or manually,thereby run below command

```
./ansible_boot.sh

```
This will automatically do the needed configurations for ansible roles and executes the ansible playbooks which setups the hdp cluster.

## Configuration:
Following Yaml configuration template structure used for configuring the playbooks  

```
---
ansible_ssh:
  user: node_username
  pass: node_password

default:
    repo_site: hosted repo site address
    dns_enabled: yes or no to update

ambari:
    hosts:
      - name: fqdn or hostname of the host for ambari instalation
        ip : ip adress of the host
    user: ambari username
    password: ambari password
    port : ambari port
    version: ambari version number

hdp:
  blueprint: blueprint name
  blueprint_configuration: blueprint specfic configuration
  stack: hdp_stack
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
  multi_node:
      host_groups:
        - host group 1:
            components:
              - component_group 1
            hosts:
                - name: fqdn or hostname of the host
                  ip : ip address of the host
            configuration: hostgroup specific configuration
            cardinality: cardinality of the group
        - host group 2:
            components:
              - component group 1
              - component group 2
            hosts:
                - name: fqdn or hostname of the host
                  ip: ip adress of the host
            configuration: hostgroup specific configuration
            cardinality: 1

hdp_test:
   hosts:
    - name: fqdn or host name of the host
   jobtracker_host: job tracker  host
   namenode_host: name node host
   oozie_host: oozie server host

postgres:
  hosts:
   - name:  fqdn or host name of the host
     ip: ip adress of the host
activemq:
  hosts:
   - name:  fqdn or host name of the host
     ip: ip adress of the host

es_master:
    hosts:
      - name: fqdn or hostname of the elastic search master node
        ip: ip address of the host

es_node:
    hosts:
      - name: fqdn or hostname of the host to setup the elastic search node
        ip: ip adress of the host

kibana:
    hosts:
      - name : fqdn or hostname of the host
       ip: ip address of the host
    elasticsearch_url: elasticsearch master host adddress
```
Please refer to the default [config file](https://engineering/bitbucket/projects/TA/repos/mdr_platform_bare_metal/browse/ansible/ambari-hdp/roles/pre-config/config.yml) being used by the existing code base
## Variables Description

Variable | example| Description
---------|----|-------
 ansible_ssh [user]| admin| node user name for ansible to login for execution of playbooks must be a sudo user
 ansible_ssh [pass]| admin| node password for ansible to use
 default[repo_site]|http://10.129.6.237/repos|Site path to hdp,ambari and the remaining packages for ambari/ansible to download during setup
 default[dns_enabled]|no| flag to updated the etc hosts if dns server is not avaible
 ambari[hosts][name]| master1-ambariserver.example.com| machine host name to setup the ambari server
 ambari[hosts][ip]|10.11.12.10| ip adress of the host machine mentioned in ambari[hosts][name]
 ambari[user]| admin| login user name of the ambari interface
 ambari[pass]| admin| login password of the ambari interface
 ambari[version]| 2.5.2.0| Ambari version number
 hdp[blueprint]| mdr-ha-blueprint| hdp cluster blueprint name
 hdp[blueprint_configuration]|zoo.cfg: [autopurge.purgeInterval: 24]| configurations specific here will be replaced in blue print configuration
 hdp[stack]|2.5| hdp stack number to be setup
 hdp[stack_version]|2.6.2.0| Full version of hdp including minimum version
 hdp[utils_version]|1.1.10.21| Full Hdp utils version
  hdp[cluster_type]|multi_node| Hdp cluster type to be formed it must be either multi_node or single_node in case of single node all compnents listed in component groups added to blueprint
 hdp[component_groups]|hive_components,[HIVE_METASTORE,HIVE_SERVER,HCAT,WEBHCAT_SERVER,HIVE_CLIENT,MYSQL_SERVER]| Component Groups is group of key as group name and array of values with the components. and this can be used in any where in any host_groups[components]. Group name based on user preference
 hdp[component_groups][component_group_name][components]|hive_components| Array of the components of that group
 hdp[multi_node][host_groups]| host groups specification and its configuration mentioned here added to the blue print
 hdp[multi_node][host_groups][host_group_name][components]|hive_components|List of the component groups mentioned in hdp[component_groups] to be added to blue print and for single node it has not effect
 hdp[multi_node][host_groups][host_group_name][hosts]|{name: agent1-ambariagent.example.com,ip:10.11.12.7}| Hosts mentioned here added to hosts list of the specific host group in the blueprint
 hdp[multi_node][host_groups][host_group_name][configuration]|| Configurations metioned here will be applied to hostgroup specific configuration in the blueprint
 hdp[multi_node][host_groups][hosts_group_name][cardinality]|1| cardinality of the host group to be added in blueprint
 hdp_test[hosts]|{name: agent1-ambariagent.example.com,ip:10.11.12.7}| hostnames of the manchines used by ansible to execute the test cases .Assuming required hdp clients are avaible on the hosts
 hdp_test[jobtracker_host]|agent8-ambariagent.example.com|Job tracker host to be used by test case job
 hdp_test[namenode_host]|agent1-ambariagent.example.com| Namenode host to be used by test case job
 hdp_test[oozie_host]|agent10-ambariagent.example.com|oozie server host to be used by test case job
  postgres[hosts]|{name: agent1-ambariagent.example.com,ip:10.11.12.7}| hostnames of the manchines used by ansible to setup postgress server
 activemq[hosts]|{name: agent1-ambariagent.example.com,ip:10.11.12.7}| hostnames of the manchines used by ansible to setup  activemq
 es_master[hosts]|{ name: master1-ambariserver.example.com,ip: 10.11.12.18 }| Hostnames and ip adress of the machines used by ansible to setup elastic search master nodes
 es_node[hosts]|{ name: agent13-ambariagent.example.com,ip: 10.11.12.23}| Hostnames and ip adress of the machines used by ansible to setup elastic search nodes
 kibana[hosts]|{ name:master1-ambariserver.example.com,ip: 10.11.12.18}| Hostnames and ip adress of the machines used by ansible to setup kibana server
 kibana[elasticsearch_url]|http://master1-ambariserver.example.com:9200 | Elastic search url to be used by the kibana



All the above mentioned Variables are mandatory and the default  [config](https://engineering/bitbucket/projects/TA/repos/mdr_platform_bare_metal/browse/ansible/ambari-hdp/roles/pre-config/config.yml) file and user needs to update as per his enviromnent specific Configurations before start using it.

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


## Licence:
mdr_platform_bare_metal - ansible - Copyright (c) 2016 BAE Systems Applied Intelligence.
