import yaml
import sys
import os
import log
import json
from config_schema import Validator
from error import MultipleInvalid,DictInvalid
from error import MatchInvalid,Invalid
validator = Validator()

try:
    import requests
except ImportError:
    REQUESTS_FOUND = False
else:
    REQUESTS_FOUND = True



def validate(configdata):
   
   log.log(log.LOG_INFO,'Validating config file')
   try:
       validator.main( configdata)
   except MultipleInvalid as e:
        for error in e.errors:
            log.log(log.LOG_ERROR, "YAML validation Error: message:{0} in {1}".format(error,configdata))
        sys.exit(1) 
   #Validate default
   log.log(log.LOG_INFO,'Validating default section')
   try:
       validator.default(configdata['default'])
   except MultipleInvalid as e:
        for error in e.errors:
            log.log(log.LOG_ERROR, "YAML validation Error default: message:{0} in {1}".format(error,configdata['default']))
        sys.exit(1)
   #Validate Ambari

   log.log(log.LOG_INFO,'Validating ambari section')

   try:
       validator.ambari(configdata['ambari'])
   except MultipleInvalid as e:
        for error in e.errors:
            log.log(log.LOG_ERROR, "YAML validation Error ambari: message:{0} in {1}".format(error,configdata['ambari']))
        sys.exit(1)
   #Validate hdp

   log.log(log.LOG_INFO,'Validating hdp section')

   try:
       validator.hdp(configdata['hdp'])
   except MultipleInvalid as e:
        for error in e.errors:
            log.log(log.LOG_ERROR, "YAML validation Error hdp: message:{0} in {1}".format(error,configdata['hdp']))
        sys.exit(1)


   #Validate add hosts
    
   log.log(log.LOG_INFO,'Validating hdp[add] section')

   hosts = configdata['hdp'].get('add',dict()).get('hosts',list())
   
   if hosts != None and len(hosts) > 0:

        try:
           validator.add(configdata['hdp']['add'])
        except MultipleInvalid as e:
           for error in e.errors:
               log.log(log.LOG_ERROR, "YAML validation Error hdp[add]: message:{0} in {1}".format(error,configdata['hdp']))
               sys.exit(1)
   
        for host in hosts:
         try:   
           validator.hosts(host)
         except MultipleInvalid as e:
           for error in e.errors:
             log.log(log.LOG_ERROR, "YAML validation Error  hdp[add][hosts]: message:{0} in {1}".format(error,host))
             sys.exit(1)

   # Validate Remove hosts
   log.log(log.LOG_INFO,'Validating hdp[remove] section')

   hosts = configdata['hdp'].get('remove',dict()).get('hosts',list())

   if hosts != None and len(hosts) > 0:

        for host in hosts:
         try:
           validator.hosts(host)
         except MultipleInvalid as e:
           for error in e.errors:
             log.log(log.LOG_ERROR, "YAML validation Error hdp[remove][hosts]: message:{0} in {1}".format(error,host))
             sys.exit(1)





def main():

    config_file = ''
    if os.path.isfile(sys.argv[1]):
        config_file = sys.argv[1]
    
    else:
        log.log(log.LOG_ERROR,"Please suply the update_hdp_cluster.yml")
        log.log(log.LOG_ERROR, "No YAML provided")
        sys.exit(1)
    try:
        config_file = open(config_file, 'r')
        try:
            config = yaml.load(config_file)
            validate(config) 
        except yaml.YAMLError, exc:
            log.log(log.LOG_ERROR, "Failed to load/parse import config YAML, Error:'{0}'".format(exc))
            log.log(log.LOG_INFO, "Check if '{0}' formatted correctly".format(config_file))
            sys.exit(1)
        config_file.close()
    except IOError as e:
        log.log(log.LOG_ERROR, "Failed to open/load import config YAML Error:'{0}'".format(e))
        log.log(log.LOG_INFO, "Check if '{0}' is available".format(config_file))
        sys.exit(1)


if __name__ == '__main__':
    main()

