#!/usr/bin/python

from schema_builder import Schema, Required,Optional,ALLOW_EXTRA
from validators import All, Length, Any,FqdnUrl,Match,Number,Unique,Componentgroups,Url,Boolean


class Validator:


    def __init__(self):

        self.config = Schema( {
            Required('ansible_ssh'): Any(dict),
            Required('default'): Any(dict),
            Optional('ambari'): All(dict),
            Optional('hdp'): All(dict),
            Optional('hdp_test'): All(dict),
            Optional('activemq'): All(dict),
            Optional('kibana'): All(dict),
            Optional('es_master'): All(dict),
            Optional('es_node'): All(dict),
            Optional('apache-server'): All(dict),
            Optional('mongodb'): All(dict),
            Optional('docker-registry'): All(dict),
            Optional('postgres'): All(dict)

        })

        self.ansible_ssh = Schema({
            Required('user'):                           All(str),
            Required('pass'):                           All(str)

        },extra=ALLOW_EXTRA )

        self.default = Schema({
            Required('repo_site'):                      All(FqdnUrl()),
            Required('dns_enabled'):                    Any(Boolean())
        },extra=ALLOW_EXTRA)

        self.ambari = Schema({
            Required('user',msg='ambari[user] doesn\'t exists'):                           Any(All(str,msg='ambari username name must be a string')),
            Required('password'):                                                           All(str),
            Required('port'):                           Any(int,msg='Port Number must be integer (Ex: 8080) but configured value'),
            Required('version'):                        Match('^[0-9]*.(\.[0-9]*){3}?$',msg='ambari version doesn''t match with expected version format( Ex: 2.5.2.0) but configured value'),
            Required('hosts',msg='ambari must have hosts configuration'):                          All(list)
        })

        self.host = Schema({
            Required('name',msg='name is doesn\'t exists'):                           All(str,msg='hostname doesnt match with the expected configured'),
            Optional('ip'):                             Match('^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$',msg='host ip does''t match with expcted ip4 version but Configured Value')
        })
        self.hdp = Schema({
            Required('blueprint',msg='hdp[blueprint] doesn\'t exists'):                             All(str),
            Required('stack',msg='hdp[statck] doesn\'t existis'):                                   Any(Number(precision=2, scale=1,yield_decimal=False,msg='hdp[stack] doesn\'t match with the exptected version format (Ex: 2.5) but configured value :') ),
            Required('default_password',msg='hdp[default_password] doesn\'t exists'):               All(str),
            Required('stack_version',msg='hdp[default_password] doesn\'t exists'):                  Match('^[0-9]*.(\.[0-9]*){3}?$',msg='hdp[stack_version] doesn\'t match with expected version format( Ex: 2.5.2.0) but configured value: '),
            Required('utils_version',msg='hdp[utils_version] doesn\'t exists'):                     Match('^[0-9]*.(\.[0-9]*){3}?$',msg='hdp[utils_version] doesn\'t match with expected version format( Ex: 1.1.0.21) but configured value: '),
            Required('cluster_name',msg='hdp[cluster_name] doensn\'t exists'):                      All(str),
            Optional('blueprint_configuration',msg='hdp[blueprint_configuration] doesn\'t exists'): Any(list,None,msg='Blueprint configuration is specific to cluster, please make sure to test it before providing here'),
            Required('component_groups',msg='hdp[component_groups] doesn\'t exists'):               Componentgroups(dict),
            Required('multi_node',msg='hdp[multi_node] doesn\'t exists'):                           All(Schema({ Required('host_groups',msg='hdp[mutli_node][host_groups] doesn\'t exists') : Any(list)})),
            Required('cluster_type',msg='hdp[cluster_type] doesn\'t exists'):                       Any('multi_node','single_node',msg='Cluster type should be multi_node or single_node')

        })

        self.component_group = Schema(Unique())
        self.host_group= Schema({
            Optional('cardinality',msg='cardinality doesn\'t exsits'):                              All(int,msg='cardinality doesn\'t match the expected'),
            Required('hosts', msg='hosts doesn\'t exsits'):                                         All(list, msg='hosts doesn\'t match the expected'),
            Required('components', msg='components doesn\'t exsits'):                               All(list, msg='components doesn\'t match the expected'),
            Optional('configuration',msg='Configuration doesn''t exists'):                          Any(list,msg='Configuration doesn\'t match the expected')
        })
        self.hdp_test = Schema({
            Required('hosts',msg='hdp_test[hosts] doesn\'t exists'):                                 All(list),
            Required('jobtracker_host',msg='hdp_test[jobtracker_host] doesn\'t exists'):             All(str,msg='jobtracker_host doesn\t match the expected'),
            Required('namenode_host',msg='hdp_test[namenode_host] doesn\'t exists'):                 All(str,msg='namenode_host doesn\t match the exptected'),
            Required('oozie_host', msg='hdp_test[oozie_host] doesn\'t exists'):                      All(str,msg='oozie_host doesn\t match the exptected')
        })
        self.kibana = Schema({
            Required('hosts',msg='kibana[hosts] doesn\t exists'):                                    All(list,msg='Doesn\'t match with expected hosts configuration'),
            Required('elasticsearch_url',msg='kibana[elasticsearch_url] doesn\'t exists'):           All(FqdnUrl(),msg='Doesn\'t match with expected elastic search url')
        })

        self.generic = Schema({
            Required('hosts',msg='hosts not mentioned'):                                            All(list,msg='Doesnt match the expected hosts configuration')
        })


