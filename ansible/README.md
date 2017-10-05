# Project:
mdr_platform_bare_metal - ansible

## Synopsis: 
This package allows us to install ansible and run the needed playbooks for installation of softwares in multiple nodes.

## Motivation: 
To get the list of host which was provisioned by foreman and install the needed softwares such as ambari and hdp through ansible into the nodes.

## Origin Repo: 
https://engineering/bitbucket/projects/TA/repos/mdr_platform_bare_metal/browse/ansible/ansible_boot.sh


## Quickstart:
Assuming that the foreman has provisioned the nodes,thereby run below command

```
./ansible_boot.sh

```
This will automatically do the needed configurations for ansible and executes the playbooks which installs the needed softwares required.

## Configuration:
Following are the configurations 

| Environment Variable       |  Example           | Description  |
|:------------- |:-------------|:-----|
|HOST_USER_NAME|root|User name of the node.|
|HOST_PASSWORD|baesystems|Password of the node.|
|FOREMAN_USER_NAME|admin|User Name of foreman|
|FOREMAN_PASSWORD|4HFefKecSjn2i7Z8|Password of foreman|
|AMBARI_SERVER_HOST_ID|ambariserver|Ambari server will be installed in host containing word ambariserver in its hostname |
|AMBARI_AGENT_HOST_ID|ambariagent|Ambari agent will be installed in host containing word ambariserver in its hostname|
|AMBARI_SERVER_ID|ambari_master| Ambari master group ID for ansible hosts |
|AMBARI_AGENT_ID|ambari_slave|Ambari slave group ID for ansible hosts |
|HDP_REPO_URL|http://10.129.6.142/repos/HDP/HDP-2.6.2.0/centos7 |This is for HDP repo path|
|HDP_UTILS_REPO_URL|http://10.129.6.142/repos/HDP/HDP-UTILS-1.1.0.21|This is for HDP utils repo path|
|AMBARI_REPO_URL|http://10.129.6.142/repos/ambari/ambari-2.5.2.0/centos7 |This is ambari repo path|
|HDP_STACK_VERSION|2.6| Stack version of HDP |
|HDP_UTILS_VERSION|1.1.0.21| HDP utils version |
|HDP_OS_TYPE|redhat7| HDP OS type |
|ENVIRONMENT|development| Development or production env |
|AMBARI_VERSION|2.5.2.0| Ambari version |



## Test:
* Once we launch `./ansible_boot.sh` ,ansible hosts file will be configured in the bootstrap machine and the servers will be grouped together as per their hostname.For example if the host name is raul-ambariservers-ambariagents.eng.vmware.com then this means the host will be acting as both ambari server and ambari agent based on the host name.If suppose  
opal-ambariagents.eng.vmware.com then this host will act only as ambari agent.This will create entry in ansible hosts `/etc/ansible/hosts` as below

```
[ambariagents]
raul-ambariservers-ambariagents.eng.vmware.com
opal-ambariagents.eng.vmware.com

[ambariservers]
raul-ambariservers-ambariagents.eng.vmware.com
```

and boostrap machine hosts `/etc/hosts` as below

```  

192.168.116.137 opal-ambariagents.eng.vmware.com
192.168.116.134 raul-ambariservers-ambariagents.eng.vmware.com

```
It also configures all other nodes hosts `/etc/hosts` so that the nodes and the bootstrap machine can recoginise each other through domain name.

* The interaction between the bootstrap machine and nodes happens through ssh where the script takes cares about public key which are added to authorized_keys in the nodes and also the nodes are under the known_hosts of the bootstrap machine which makes the bootstrap machine to access other nodes.

* It also configures the ansible call back plugin for foreman so that the software configuration management interaction between the bootstrap machine and the nodes can be known through foreman.

* It also executes the playbook setup for ambari server and ambari agents which installs the ambari severs and agents according to the host group for the nodes.This can be also verified as below

```
[root@foreman abbc]# ssh root@raul-ambariservers-ambariagents.eng.vmware.com
Last login: Wed Aug 16 23:34:41 2017 from foreman.eng.vmware.com
[root@raul-ambariservers-ambariagents ~]# ps -ef | grep ambari
root      20941      1  3 Aug15 ?        01:28:22 /usr/jdk64/jdk1.8.0_60/bin/java -server -XX:NewRatio=3 -XX:+UseConcMarkSweepGC -XX:-UseGCOverheadLimit -XX:CMSInitiatingOccupancyFraction=60 -Dsun.zip.disableMemoryMapping=true -Xms512m -Xmx2048m -Djava.security.auth.login.config=/etc/ambari-server/conf/krb5JAASLogin.conf -Djava.security.krb5.conf=/etc/krb5.conf -Djavax.security.auth.useSubjectCredsOnly=false -cp /etc/ambari-server/conf:/usr/lib/ambari-server/*:/usr/share/java/postgresql-jdbc.jar org.apache.ambari.server.controller.AmbariServer
postgres  20957  20713  0 Aug15 ?        00:00:00 postgres: ambari ambari 127.0.0.1(40233) idle

```

* This script also launches the HDP multi-node configuration dynamically according to host name of the nodes which are grouped as ambari servers and ambari agents .This also forms the HDP cluster which can be viewed through UI in bootstrap machine as below

```

http://raul-ambariservers-ambariagents.eng.vmware.com:8080/#/main/dashboard/metrics


```

## Licence:
mdr_platform_bare_metal - ansible - Copyright (c) 2016 BAE Systems Applied Intelligence.

