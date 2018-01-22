#!/usr/bin/python

from schema_builder import Schema, Required,Optional,ALLOW_EXTRA
from validators import All, Length, Any,FqdnUrl,Match,Number,Unique,Componentgroups,Url,Boolean


class Validator:


    def __init__(self):

       self.main = Schema({
	  Required('default',msg='default doesn\'t exists'): Any(dict),
          Required('es_master',msg='es_master section doesn\'t exists'): Any(dict),
          Required('es_node',msg='es_node section doesn\\t exists'): All(dict)

       }) 
       self.default = Schema({
            Required('dns_enabled',msg='default[dns_enabled] doesn\'t exists'):             Any(Boolean(),msg='dns_enable must be either yes or no'),
            Optional('java_vendor'):                                                       Any('oracle','openjdk',msg='must be either oracle or openjdk')
        })

       self.es_master = Schema({
            Required('host',msg='es_master[host] doesn\'t exists'):                        Any(str,msg='host must be a string'),
            Required('version',msg='es_master[version] doesn\'t exists'):                  Match('^[0-9]*.(\.[0-9]*){2}?$',msg='es_master version doesn''t match with expected version format( Ex: 5.5 ) but configured value'),
            Required('es_heap_size',msg='es_master[es_heap_size] doesn\'t exists'):          Any(str,msg='es heap size must be a string ex: 1g'),
            Optional('es_config',msg='es_master[es_config] doesn\'t exists'):              Any(dict)
        })


       self.es_node = Schema({
            Optional('add'):                                       Any(dict),
            Optional('remove'):                                    Any(dict),
            Required('es_config'):                                 Any(dict),
            Required('es_api_port',msg='es_master[es_api_port] doesn\'t exists'):          Any(int,msg='Port Number must be integer (Ex: 9200) but configured value'),

        })
       self.es_config = Schema({
           Required('network.host',msg='es_master[es_config][network.host] doesn\'t exists'):   Any('_[networkInterface]_','_local_','_site_','_global_',msg='The options must be one of:_[networkInterface]_,_local_,_site_,_global_'),
           Required('cluster.name',msg='es_maste[es_config][cluster.name] doesn\'t exists'):                        Any(str,msg='cluster.name must be a string'),
           Required('http.port',msg='es_master[es_config][http.port] doesn\'t exists'):          Any(int,msg='http.port Number must be integer (Ex: 9200) but configured value'),
           Required('transport.tcp.port',msg='es_master[es_config][transport.tcp.port] doesn\'t exists'):          Any(int,msg='transport.tcp.port Number must be integer (Ex: 9300) but configured value'),
           Required('node.data',msg='es_master[es_config][node.data] doesn\t exists'):             Any(Boolean(),msg='node.data must be either true or false'),
           Required('node.master',msg='es_master[es_config][master.data] doesn\t exists'):             Any(Boolean(),msg='node.master must be either true or false'),
           Required('bootstrap.memory_lock',msg='es_master[es_config][bootstrap.memory_lock] doesn\t exists'):             Any(Boolean(),msg='bootstrap.memory_lock must be either true or false')
      },extra=ALLOW_EXTRA)


       self.hosts= Schema({
           Required('name',msg='name is required'):                                    All(str,msg='name(hostname) must be a sring'),
           Optional('ip'):                                                             Match(
                '^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$',msg='host ip does''t match with expcted ip4 version but Configured Value')
            })
       
      
  
