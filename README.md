# Project:
mdr_platform_bare_metal - ansible

## Synopsis: 
This package allows us to install ansible and run the needed playbooks for installation of softwares in multiple nodes.

## Motivation: 
To get the list of host which was provisioned by foreman and install the needed softwares such as ambari and hdp through ansible into the nodes.

## Origin Repo: 
https://engineering/bitbucket/projects/TA/repos/mdr_platform_bare_metal/browse/boot_ansible_hadoop.sh


## Quickstart:
Assuming that the foreman has provisioned the nodes,thereby run below command

```
./boot_ansible_hadoop.sh

```
This will do automatically the needed configuartions for ansible and also executes the playbooks which installs the needed softwares required.

## Configuration:
Following are the configurations 

| Environment Variable       |  Example           | Description  |
|:------------- |:-------------|:-----|
|HOST_USER_NAME|root|User name of the host.|
|HOST_PASSWORD|baesystems|Password of the host.|
|FTP_URL|ftp://192.168.116.130|ftp server url|
|ANSIBLE_HADOOP_PATH|${FTP_URL}/pub/ansible-hadoop-master/*|Path of the hadoop playbooks in ftp server|
|ANSIBLE_HDP_PATH|${FTP_URL}/pub/blueprints/*|Path of the hdp playbooks in ftp server|
|FOREMAN_CALLBACK_PATH|${FTP_URL}/pub/foreman_callback.py|Path of foreman_callback.py file in ftp server|
|PROXY_URL|http://10.129.49.21:8080| Proxy used. |
|AMBARI_SERVER_ID|ambariservers|This ID will be compared with the hostname to determine whether the host belong to ambari server group. |
|AMBARI_AGENT_ID|ambariagents|This ID will be compared with the hostname to determine whether the host belong to ambari agent group.|
|AMBARI_USER_NAME|admin|User name of ambari login.|
|AMBARI_PASSWORD|admin|Password of ambari login. |



## Test:
* Once we launch `./boot_ansible_hadoop.sh` ,ansible hosts file will be configured in the bootstrap machine and the servers will be grouped together as per their hostname.For example if the host name is raul-ambariservers-ambariagents.eng.vmware.com then this means the host will be acting as both ambari server and ambari agent based on the host name.If suppose  
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

