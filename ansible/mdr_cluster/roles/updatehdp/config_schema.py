#!/usr/bin/python

from schema_builder import Schema, Required,Optional,ALLOW_EXTRA
from validators import All, Length, Any,FqdnUrl,Match,Number,Unique,Componentgroups,Url,Boolean


class Validator:


    def __init__(self):

       self.main = Schema({
	  Required('default',msg='default doesn\'t exists'): Any(dict),
          Required('ambari',msg='ambari doesn\'t exists'): Any(dict),
          Required('hdp',msg='hdp doesn\\t exists'): All(dict)

       }) 
       self.default = Schema({
            Required('dns_enabled',msg='default[dns_enabled] doesn\'t exists'):             Any(Boolean(),msg='dns_enable must be either yes or no'),
            Optional('java_vendor'):                                                       Any('oracle','openjdk',msg='must be either oracle or openjdk')
        })

       self.ambari = Schema({
            Required('port',msg='ambari[port] doesn\'t exists'):                           Any(int,msg='Port Number must be integer (Ex: 8080) but configured value'),
            Required('version',msg='ambari[version] doesn\'t exists'):                     Match('^[0-9]*.(\.[0-9]*){3}?$',msg='ambari version doesn''t match with expected version format( Ex: 2.5.2.0) but configured value'),
	    Required('host','ambari[host] doesn\'t exists'):                               All(str,msg='Hostname must be a string')
        })


       self.hdp = Schema({
           Required('clustername',msg='hdp[clustername] doesn\'t exists'):                  All(str,msg='Clustername must be a string'),
           Required('blueprint',msg='hdp[blueprint] doesn\'t exists'):                      All(str,msg='blueprint must be a string'),
           Optional('add'):                                                                Any(dict),
           Optional('remove'):                                                             Any(dict)

        })

       self.hosts= Schema({
           Required('name',msg='name is required'):                                    All(str,msg='name(hostname) must be a sring'),
           Optional('ip'):                                                             Match(
                '^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$',msg='host ip does''t match with expcted ip4 version but Configured Value')
            })
       
       self.add = Schema({
	 Required('hosts'):                                                             Any(list),
         Required('hostgroup',msg='hostgroup doesn\'t exists'):                           All(str,msg='hostgroup must be a string')
	})
       self.remove = Schema({
         Optional('hosts'):                                                              Any(list)                                                                    
        })
      
  
