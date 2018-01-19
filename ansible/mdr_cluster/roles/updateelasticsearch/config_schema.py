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
            Required('version',msg='es_master[version] doesn\'t exists'):                  Match('^[0-9]*.(\.[0-9]*){2}?$',msg='es_master version doesn''t match with expected version format( Ex: 5.5 ) but configured value')
        })


       self.es_node = Schema({
            Optional('add'):                                       Any(dict),
            Optional('remove'):                                    Any(dict),
            Required('es_config'):                                 Any(dict)
        })


       self.hosts= Schema({
           Required('name',msg='name is required'):                                    All(str,msg='name(hostname) must be a sring'),
           Optional('ip'):                                                             Match(
                '^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$',msg='host ip does''t match with expcted ip4 version but Configured Value')
            })
       
      
  
