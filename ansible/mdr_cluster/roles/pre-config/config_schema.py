#!/usr/bin/python

from schema_builder import Schema, Required,Optional,ALLOW_EXTRA
from validators import All, Length, Any,FqdnUrl,Match,Number,Unique,Componentgroups,Url,Boolean


class Validator:


    def __init__(self):

        self.common = Schema({
            Required('hostgroups',msg='hostgroups doesn\'t exists'): Any(list,msg='each hostgroup  must be as an array element'),
            Required('primary_hosts', msg='hostgroups doesn\'t exists'): All(list)
        },extra=ALLOW_EXTRA)

        self.common_hostgroup = Schema({
            Required('name','host group name is required in common[hostgroups]'): All(str,msg='hostgroup name must be a string'),
            Required('domain', 'domain name is required in common[hostgroups]'): Match('^[a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9]\.[a-zA-Z]{2,}$',msg='domain doesn\'t match expected value ex: example.com but configured value'),
        },extra=ALLOW_EXTRA)

        self.common_primary_host = Schema({
            Required('name', 'host group name is required in common[hostgroups]'): All(str,msg='hostgroup name must be a string'),
            Required('ip','ip is required for in common[primary_hosts]'): Match(
                '^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$',msg='host ip does''t match with expcted ip4 version but Configured Value'),

        }, extra=ALLOW_EXTRA)

        self.config = Schema( {
            Required('default',msg='default doesn\'t exists'): Any(dict),
            Required('common',msg='common doesn\'t exists'): Any(dict),
            Optional('ambari'): All(dict),
            Optional('hdp'): All(dict),
            Optional('hdp_test'): All(dict),
            Optional('activemq'): All(dict),
            Optional('kibana'): All(dict),
            Optional('es_master'): All(dict),
            Optional('es_node'): All(dict),
            Optional('apache'): All(dict),
            Optional('mongodb'): All(dict),
            Optional('docker'): All(dict),
            Optional('postgres'): All(dict)
        },extra=ALLOW_EXTRA)

        self.default = Schema({
            Required('dns_enabled',msg='default[dns_enabled] doesn\t exists'):             Any(Boolean(),msg='dns_enable must be either yes or no'),
            Optional('java_vendor'):                                                       Any('oracle','openjdk',msg='must be either oracle or openjdk')
        })

        self.hdpambari = Schema({
            Required('ambari','ambari needs to be specified if hdp is configured'): Any(dict,msg='ambari configuratin doesn\'t match the expected format expected is dictionary') ,
            Required('hdp', 'hdp needs to be specified if ambari is configured'): Any(dict,
                                                                                         msg='hdp configuratin doesn\'t match the expected format expected is dictionary')
        },extra=ALLOW_EXTRA)
        self.ambari = Schema({
            Required('port',msg='ambari[port] doesn\'t exists'):                                                              Any(int,msg='Port Number must be integer (Ex: 8080) but configured value'),
            Required('version',msg='ambari[version] doesn\'t exists'):                                                           Match('^[0-9]*.(\.[0-9]*){3}?$',msg='ambari version doesn''t match with expected version format( Ex: 2.5.2.0) but configured value'),
            Required('hostgroup',msg='ambari must have hosts configuration'):              All(str,msg='hostgroup in ambari must be a string and must configured in common[hostgroups] as well')
        },extra=ALLOW_EXTRA)

        self.hdp = Schema({
            Required('blueprint',msg='hdp[blueprint] doesn\'t exists'):                             All(str,msg='blueprint shuld be string ex: mdr-ha-blueprint'),
            Required('stack',msg='hdp[statck] doesn\'t existis'):                                   Any(Number(precision=2, scale=1,yield_decimal=False,msg='hdp[stack] doesn\'t match with the exptected version format (Ex: 2.5) but configured value :') ),
            Required('stack_version',msg='hdp_stackversion doesn\'t exists'):                  Match('^[0-9]*.(\.[0-9]*){3}?$',msg='hdp[stack_version] doesn\'t match with expected version format( Ex: 2.5.2.0) but configured value: '),
            Required('utils_version',msg='hdp[utils_version] doesn\'t exists'):                     Match('^[0-9]*.(\.[0-9]*){3}?$',msg='hdp[utils_version] doesn\'t match with expected version format( Ex: 1.1.0.21) but configured value: '),
            Required('cluster_name',msg='hdp[cluster_name] doensn\'t exists'):                      All(str,msg='cluster_name must be a string ex: mdr'),
            Optional('blueprint_configuration',msg='hdp[blueprint_configuration] doesn\'t exists'): Any(list,None,msg='Blueprint configuration is specific to cluster, please make sure to test it before providing here'),
            Required('component_groups',msg='hdp[component_groups] doesn\'t exists'):               Componentgroups(dict),
            Required('hostgroups',msg='hdp[hostgroups] doesn\'t exists'):                           All(list,msg='hostgroup doesn\'t match the expected format'),
            Required('cluster_type',msg='hdp[cluster_type] doesn\'t exists'):                       Any('multi_node','single_node',msg='Cluster type should be multi_node or single_node')

        })

        self.component_group = Schema(Unique())
        self.host_group= Schema({
            Required('hostgroup', msg='hostgroup doesn\'t exsits'):                                    Any(str, msg='hostgroup name must be a string'),
            Required('components', msg='components doesn\'t exsits'):                               All(list, msg='components doesn\'t match the expected'),
            Optional('configuration',msg='Configuration doesn''t exists'):                          Any(dict,msg='Configuration doesn\'t match the expected'),
            Optional('cardinality', msg='cardinality doesn\'t exsits'):                             All(int,msg='cardinality must be an integer'),
        })
        self.hdp_test = Schema({
            Required('hostgroup',msg='hdp_test[hostgroup] doesn\'t exists'):                         All(str,msg='hostgroup must be a string'),
            Required('jobtracker_host',msg='hdp_test[jobtracker_host] doesn\'t exists'):             All(str,msg='jobtracker_host doesn\t match the expected'),
            Required('namenode_host',msg='hdp_test[namenode_host] doesn\'t exists'):                 All(str,msg='namenode_host doesn\t match the exptected'),
            Required('oozie_host', msg='hdp_test[oozie_host] doesn\'t exists'):                      All(str,msg='oozie_host doesn\t match the exptected')
        })
        self.kibana = Schema({
            Required('hostgroup',msg='kibana[hosts] doesn\t exists'):                                    All(str,msg='hostgroup must be a string'),
            Required('elasticsearch_url',msg='kibana[elasticsearch_url] doesn\'t exists'):           All(FqdnUrl(),msg='Doesn\'t match with expected elastic search url'),
            Required('version',msg='kibana[version] doesn\'t exists'):                                                           Match('^[0-9]*.(\.[0-9]*){2}?$',msg='kibana version doesn''t match with expected version format( Ex: 5.5.0) but configured value')
        })
        self.postgres = Schema({
            Required('hostgroup',msg='postgres[hosts] doesn\t exists'):                                    All(str,msg='hostgroup must be a string'),
            Required('version',msg='postgres[version] doesn\'t existis'):                                   Any(Number(precision=2, scale=1,yield_decimal=False,msg='postgres[version] doesn\'t match with the exptected version format (Ex: 9.6) but configured value') )
        })
 
        self.es_master = Schema({
            Required('hostgroup',msg='postgres[hosts] doesn\t exists'):                                    All(str,msg='hostgroup must be a string'),
            Required('version',msg='es_master[version] doesn\'t exists'):                  Match('^[0-9]*.(\.[0-9]*){2}?$',msg='es_master version doesn''t match with expected version format( Ex: 5.5 ) but configured value'),
            Required('es_heap_size',msg='es_master[es_heap_size] doesn\'t exists'):          Any(str,msg='es heap size must be a string ex: 1g'),
            Optional('es_config',msg='es_master[es_config] doesn\'t exists'):              Any(dict)
        })


        self.es_node = Schema({
            Required('hostgroup',msg='postgres[hosts] doesn\t exists'):                                    All(str,msg='hostgroup must be a string'),
            Required('es_config'):                                 Any(dict),
            Required('es_api_port',msg='es_master[es_api_port] doesn\'t exists'):          Any(int,msg='Port Number must be integer (Ex: 9200) but configured value'),

        })
        self.es_config = Schema({
           Required('network.host',msg='es_master[es_config][network.host] doesn\'t exists'):   Match('^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$',msg='network.host does\'t match with expected ip4 version but Configured Value'),
           Required('cluster.name',msg='es_maste[es_config][cluster.name] doesn\'t exists'):                        Any(str,msg='cluster.name must be a string'),
           Required('http.port',msg='es_master[es_config][http.port] doesn\'t exists'):          Any(int,msg='http.port Number must be integer (Ex: 9200) but configured value'),
           Required('transport.tcp.port',msg='es_master[es_config][transport.tcp.port] doesn\'t exists'):          Any(int,msg='transport.tcp.port Number must be integer (Ex: 9300) but configured value'),
           Required('node.data',msg='es_master[es_config][node.data] doesn\t exists'):             Any(Boolean(),msg='node.data must be either true or false'),
           Required('node.master',msg='es_master[es_config][master.data] doesn\t exists'):             Any(Boolean(),msg='node.master must be either true or false'),
           Required('bootstrap.memory_lock',msg='es_master[es_config][bootstrap.memory_lock] doesn\t exists'):             Any(Boolean(),msg='bootstrap.memory_lock must be either true or false')})

        self.apache = Schema({
            Required('hostgroup',msg='apache[hosts] doesn\t exists'):                                    All(str,msg='hostgroup must be a string'),
 Required('httpd_version',msg='apache[httpd_version] doesn\'t exists'):                                                           Match('^[0-9]*.(\.[0-9]*){2}?$',msg='httpd version doesn''t match with expected version format( Ex: 2.4.6) but configured value'),
Required('tomcat_version',msg='apache[tomcat_version] doesn\'t exists'):                                                           Match('^[0-9]*.(\.[0-9]*){2}?$',msg='tomcat version doesn''t match with expected version format( Ex: 7.0.76) but configured value')
        })
        self.mongodb = Schema({
            Required('hostgroup',msg='mongodb[hosts] doesn\t exists'):                                    All(str,msg='hostgroup must be a string'),
             Required('version',msg='mongodb[version] doesn\'t exists'):                                                           Match('^[0-9]*.(\.[0-9]*){2}?$',msg='mongodb version doesn''t match with expected version format( Ex: 3.4.10) but configured value')
        })
        self.activemq = Schema({
            Required('hostgroup', msg='activemq[hosts] doesn\t exists'): All(str, msg='hostgroup must be a string'),
           Required('version',msg='activemq[version] doesn\'t exists'):                                                           Match('^[0-9]*.(\.[0-9]*){2}?$',msg='activemq version doesn''t match with expected version format( Ex: 5.15.0) but configured value')
        })

        self.docker = Schema({
            Required('hostgroup',msg='docker[hosts] doesn\t exists'):                                    All(str,msg='hostgroup must be a string'),
            Required('version',msg='docker[version] doesn\'t exists'):                                                           Match('^[0-9]*.(\.[0-9]*){2}?$',msg='docker version doesn''t match with expected version format( Ex: 17.09.0) but configured value')
        })


