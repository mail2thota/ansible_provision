#!/usr/bin/python
# -*- coding: utf8 -*-
#Copyright:@BaeSystemsAI
#Original author: Heri Sutrisno
#Email:harry.sutrisno@baesystems.com
#Description:payload foreman resources

import sys
import logging
import log
from pprint import pprint
from validator import Validator
from voluptuous import MultipleInvalid

class ForemanLoad:
    
    def __init__(self, config, loglevel=logging.INFO):
        logging.basicConfig(level=loglevel)
        log.LOGLEVEL = loglevel
        self.loglevel = loglevel
        try:
            validyml='common'
            if type(config[validyml]) is not dict:
                raise
            validyml='foreman'
            if type(config[validyml]) is not dict:
                raise
        except:
            log.log(log.LOG_ERROR, "Section '{0}' is required: YAML validation Error".format(validyml))
            log.log(log.LOG_ERROR, "Section '{0}' type unknown, it must be key and value: YAML validation Error".format(validyml))
            sys.exit(1)

        self.config = config['foreman']
        self.common =  config['common']
        self.validator = Validator()
       
    def validate_main_yml(self):
        log.log(log.LOG_INFO, "Validate Foreman Main YML")
        try:
           validyml='auth'
           if type(self.config[validyml]) is not dict:
               raise
           validyml='domain'
           if type(self.config[validyml][0]) is not dict:
               raise
           validyml='subnet'
           if type(self.config[validyml][0]) is not dict:
               raise
           validyml='hostgroups'
           if type(self.common[validyml][0]) is not dict:
               raise
           validyml='primary_hosts'
           if type(self.common[validyml][0]) is not dict:
               raise
           validyml='secondary_hosts'
           self.ifexist=False
           if validyml in self.common:
               self.ifexist=True
               if type(self.common[validyml][0]) is not dict:
                   raise
           validyml='protocol'
           if type(self.config[validyml]) is not dict:
               raise
           validyml='foreman_proxy'
           if type(self.config[validyml]) is not dict:
               raise
           validyml='architecture'
           if type(self.config[validyml][0]) is not dict:
               raise
           validyml='medium'
           if type(self.config[validyml][0]) is not dict:
               raise
           validyml='setting'
           if type(self.config[validyml][0]) is not dict:
               raise
           validyml='os'
           if type(self.config[validyml][0]) is not dict:
               raise
           validyml='hostgroup_system'
           if type(self.config[validyml]) is not dict:
               raise
           validyml='partition_system'
           if type(self.config[validyml]) is not dict:
               raise
           validyml='partition_table'
           if type(self.config[validyml][0]) is not dict:
               raise
        except: 
            log.log(log.LOG_ERROR, "Section '{0}' is required: YAML validation Error".format(validyml))
            log.log(log.LOG_ERROR, "Section '{0}' type unknown, it must be key and value: YAML validation Error".format(validyml))
            sys.exit(1)
        
    def get_config_section(self, section):

        try:
            cfg = self.config[section]
        except:
            log.log(log.LOG_ERROR, "Cannot find section '{0}' in yml file, it is mandatory".format(section))
            sys.exit(1)

        return cfg

    def get_common_section(self, section):

        try:
            cfg = self.common[section]
        except:
            log.log(log.LOG_ERROR, "Cannot find section '{0}' in yml file, it is mandatory".format(section))
            sys.exit(1)

        return cfg

    def linearSearch(self,item,my_list):
        found = False
        position = 0
        while position < len(my_list) and not found:
            if my_list[position] == item:
                found = True
            position = position + 1
        return found
 
    def validate_auth(self):
        log.log(log.LOG_INFO, "Validate Auth")
        auth=self.get_config_section('auth')
        try:
            self.validator.auth(auth)
        except MultipleInvalid as e:
            log.log(log.LOG_ERROR, "Cannot create auth '{0}': \n YAML validation Error: {1}".format(auth, e))
            sys.exit(1)
         
    def validate_config_arch(self):
        log.log(log.LOG_INFO, "Validate Architectures")
        list_arch=[]
        for arch in self.get_config_section('architecture'):
            try:
                self.validator.arch(arch)
                itemFound = self.linearSearch(arch['name'],list_arch)
                if itemFound:
                    log.log(log.LOG_ERROR,"architecture name: {0} is already set,duplication is not allowed".format(arch['name']))
                    sys.exit(1)
                list_arch.append(arch['name'])
            except MultipleInvalid as e:
                log.log(log.LOG_ERROR, "Cannot create Architecture '{0}' \n YAML validation Error: {1}".format(arch, e))
                sys.exit(1)


    def validate_config_domain(self):
        log.log(log.LOG_INFO, "Validate Domains")
        list_domain=[]
        for domain in self.get_config_section('domain'):
            try:
                self.validator.domain(domain)
                itemFound = self.linearSearch(domain['name'],list_domain)
                if itemFound:
                    log.log(log.LOG_ERROR,"domain name: {0} is already set,duplication is not allowed".format(domain['name']))
                    sys.exit(1)                              
                list_domain.append(domain['name'])
            except MultipleInvalid as e:
                log.log(log.LOG_ERROR, "Cannot create Domain '{0}' \n YAML validation Error: {1}".format(domain, e))
                sys.exit(1)

    def validate_config_medium(self):
        log.log(log.LOG_INFO, "Validate Media")
        list_medium=[]
        for medium in self.get_config_section('medium'):
            try:
                self.validator.medium(medium)
                itemFound = self.linearSearch(medium['name'],list_medium)
                if itemFound:
                    log.log(log.LOG_ERROR,"medium name: {0} is already set,duplication is not allowed".format(medium['name']))
                    sys.exit(1)
                list_medium.append(medium['name'])
            except MultipleInvalid as e:
                log.log(log.LOG_ERROR, "Cannot create Media '{0}': \n YAML validation Error: {1}".format(medium, e))
                sys.exit(1)
            

    def validate_config_settings(self):
        log.log(log.LOG_INFO, "Validate Foreman Settings")
        list_setting=[]
        for setting in self.get_config_section('setting'):
            try:
                self.validator.setting(setting)
                itemFound = self.linearSearch(setting['name'],list_setting)
                if itemFound:
                    log.log(log.LOG_ERROR,"setting name: {0} is already set,duplication is not allowed".format(setting['name']))
                    sys.exit(1)
                list_setting.append(setting['name'])

            except MultipleInvalid as e:
                log.log(log.LOG_ERROR, "Cannot create Setting '{0}': \n YAML validation Error: {1}".format(setting, e))
                sys.exit(1)

    def validate_protocol(self):
        log.log(log.LOG_INFO, "Validate Protocol")
        protocol = self.get_config_section('protocol')
        try: 
            self.validator.protocol(protocol) 
        except MultipleInvalid as e:
            log.log(log.LOG_ERROR, "Cannot create protocol '{0}': \n YAML validation Error '{1}'".format(protocol, e))
            sys.exit(1)


    def validate_config_smartproxy(self):
        log.log(log.LOG_INFO, "Validate Smart Proxies")
        fmproxy = self.get_config_section('foreman_proxy')
        try: 
            self.validator.foreman_proxy(fmproxy) 
        except MultipleInvalid as e:
            log.log(log.LOG_ERROR, "Cannot create foreman-proxy '{0}': \n YAML validation Error '{1}'".format(fmproxy, e))
            sys.exit(1)
   

    def validate_mutual_exclusive(self,section,name):
        log.log(log.LOG_INFO, "Validate Mutual Exclusive Of Sections")
        if section in self.common:
            for items in self.get_common_section(section):
                if items['name'] == name:
                    return True 

            log.log(log.LOG_ERROR, "'{0}'was not found in the list of YAML section: '{1}'".format(name,section))
            sys.exit(1)
 
        for items in self.get_config_section(section):
             if items['name'] == name:
                 return True
        
        log.log(log.LOG_ERROR, "'{0}'was not found in the list of YAML section: '{1}'".format(name,section))
        sys.exit(1)

 
    def validate_config_subnet(self):
        log.log(log.LOG_INFO, "Validate Subnets")
        list_subnet=[]
        for subnet in self.get_config_section('subnet'):
            try:
                self.validator.subnet(subnet)
                itemFound = self.linearSearch(subnet['name'],list_subnet)
                if itemFound:
                    log.log(log.LOG_ERROR,"subnet name: {0} is already set,duplication is not allowed".format(subnet['name']))
                    sys.exit(1)
                list_subnet.append(subnet['name'])
            except MultipleInvalid as e:
                log.log(log.LOG_ERROR, "Cannot create Subnet '{0}': \n YAML validation Error: {1}".format(subnet, e))
                sys.exit(1)
            list_domain= []
            for domain in subnet['domain']:
                dname=domain['name']
                self.validate_mutual_exclusive('domain',dname)
                itemFound = self.linearSearch(domain['name'],list_domain)
                if itemFound:
                    log.log(log.LOG_ERROR,"domain name: {0} is already set in subnet section,duplication is not allowed".format(domain['name']))
                    sys.exit(1)
                list_domain.append(domain['name'])

 

    def validate_config_os(self):
        log.log(log.LOG_INFO, "Validate Operating Systems")
        list_os=[]
        for operatingsystem in self.get_config_section('os'):
            try:
                self.validator.os(operatingsystem)
                itemFound = self.linearSearch(operatingsystem['name'],list_os)
                if itemFound:
                    log.log(log.LOG_ERROR,"operating system name: {0} is already set,duplication is not allowed".format(operatingsystem['name']))
                    sys.exit(1)
                list_os.append(operatingsystem['name'])
            except MultipleInvalid as e:
                log.log(log.LOG_ERROR, "Cannot create Operating System '{0}': \n YAML validation Error: {1}".format(operatingsystem, e))
                sys.exit(1)
            list_arch=[]
            for arches in operatingsystem['architecture']:
                archname=arches['name']
                self.validate_mutual_exclusive('architecture',archname)
                itemFound = self.linearSearch(arches['name'],list_arch)
                if itemFound:
                    log.log(log.LOG_ERROR,"architecture name: {0} is already set in os section,duplication is not allowed".format(arches['name']))
                    sys.exit(1)
                list_arch.append(arches['name'])
            list_medias=[]
            for medias in operatingsystem['medium']:
                mdname=medias['name']
                self.validate_mutual_exclusive('medium',mdname)
                itemFound = self.linearSearch(medias['name'],list_medias)
                if itemFound:
                    log.log(log.LOG_ERROR,"medium name: {0} is already set in os section,duplication is not allowed".format(medias['name']))
                    sys.exit(1)
                list_medias.append(medias['name'])


    def validate_config_hostgroup(self):
        log.log(log.LOG_INFO, "Validate Hostgroups System")
        hostg_system=self.get_config_section('hostgroup_system')
        try:
            self.validator.hostgroup_system(hostg_system)
        except MultipleInvalid as e:
            log.log(log.LOG_ERROR, "Cannot create hostgroup_system '{0}': \n YAML validation Error: {1}".format(hostg_system, e))
            sys.exit(1)
        osname=hostg_system['os']
        self.validate_mutual_exclusive('os',osname)
        archname=hostg_system['architecture']
        self.validate_mutual_exclusive('architecture',archname)
        mdname=hostg_system['medium']
        self.validate_mutual_exclusive('medium',mdname)


        log.log(log.LOG_INFO, "Validate Hostgroups")
        list_hostg=[]
        for hostgroup in self.get_common_section('hostgroups'):
            try:
                self.validator.hostgroup(hostgroup)
                itemFound = self.linearSearch(hostgroup['name'],list_hostg)
                if itemFound:
                    log.log(log.LOG_ERROR,"hostgroup name: {0}is already set,duplication is not allowed".format(hostgroup['name']))
                    sys.exit(1)
                list_hostg.append(hostgroup['name'])
            except MultipleInvalid as e:
                log.log(log.LOG_ERROR, "Cannot create Hostgroup '{0}': \n YAML validation Error: {1}".format(hostgroup, e))
                sys.exit(1)
            
            sbname=hostgroup['subnet']
            self.validate_mutual_exclusive('subnet',sbname)
            dname=hostgroup['domain']
            self.validate_mutual_exclusive('domain',dname)
            ptable_name=hostgroup['partition_table']
            self.validate_mutual_exclusive('partition_table',ptable_name)


    def validate_config_ptable(self):
        log.log(log.LOG_INFO, "Validate Partition Table")
        list_ptable=[]
        for ptable in self.get_config_section('partition_table'):
            try:
                self.validator.ptable(ptable)
                itemFound = self.linearSearch(ptable['name'],list_ptable)
                if itemFound:
                    log.log(log.LOG_ERROR,"ptable name: {0} is already set,duplication is not allowed".format(ptable['name']))
                    sys.exit(1)
                list_ptable.append(ptable['name'])
            except MultipleInvalid as e:
                log.log(log.LOG_ERROR, "Cannot create Partition Table '{0}' \n YAML validation Error: {1}".format(ptable, e))
                sys.exit(1)
        for ptable in self.get_config_section('partition_table'):
            try:
               boot= ptable['boot']['size']
               swap= ptable['swap']['size']
               tmp= ptable['tmp']['size']
               var= ptable['var']['size']
               home= ptable['home']['size']
               root= ptable['root']['size']
               percent_t=boot+swap+tmp+var+home+root
               if percent_t > 100:
                   log.log(log.LOG_ERROR, "size of 'boot+swap+tmp+var+home+root' must be <= 100%".format(ptable))               
                   raise
            except:
                log.log(log.LOG_ERROR, "Cannot create Partition Table '{0}'".format(ptable))
                sys.exit(1)

        

    def load_config_primaryhosts(self):
        log.log(log.LOG_INFO, "Validate Primary Hosts")
        list_primary=[]
        for hostc in self.get_common_section('primary_hosts'):
            try:
                self.validator.primary_hosts(hostc)
                itemFound = self.linearSearch(hostc['name'],list_primary)
                if itemFound:
                    log.log(log.LOG_ERROR,"primary host name: {0} is already set,duplication is not allowed".format(hostc['name']))
                    sys.exit(1)
                list_primary.append(hostc['name'])
            except MultipleInvalid as e :
                log.log(log.LOG_ERROR, "Cannot create primary hosts '{0}': \n YAML validation Error: {1}".format(hostc, e))
                sys.exit(1)
            hgname=hostc['hostgroup']
            self.validate_mutual_exclusive('hostgroups',hgname)

    def load_config_secondaryhosts(self):
        if self.ifexist:
            log.log(log.LOG_INFO, "Validate Secondary Hosts")
            for hostc in self.get_common_section('secondary_hosts'):
                try:
                    self.validator.secondary_hosts(hostc)
                except MultipleInvalid as e :
                    log.log(log.LOG_ERROR, "Cannot create secondary hosts '{0}': \n YAML validation Error: {1}".format(hostc, e))
                    sys.exit(1)
                sbname=hostc['subnet']
                self.validate_mutual_exclusive('subnet',sbname)
                hostname=hostc['primary']
                self.validate_mutual_exclusive('primary_hosts',hostname)

    def validate_ipmac(self):
        log.log(log.LOG_INFO, "Validate IP And Mac Duplication")
        list_ip=[]
        list_mac=[]        
        if self.ifexist:
            for secondary in self.get_common_section('secondary_hosts'):
                 itemFound = self.linearSearch(secondary['ip'],list_ip)
                 if itemFound:
                     log.log(log.LOG_ERROR,"host ip: {0} is already set,duplication is not allowed".format(secondary['ip']))
                     sys.exit(1)
                 itemFound = self.linearSearch(secondary['mac'],list_mac)
                 if itemFound:
                    log.log(log.LOG_ERROR,"host mac: {0} is already set,duplication is not allowed".format(secondary['mac']))
                    sys.exit(1)
                 list_ip.append(secondary['ip']) 
                 list_mac.append(secondary['mac'])
          
        for primary in self.get_common_section('primary_hosts'):
            itemFound = self.linearSearch(primary['ip'],list_ip)
            if itemFound:
                    log.log(log.LOG_ERROR,"host ip: {0} is already set,duplication is not allowed".format(primary['ip']))
                    sys.exit(1)
            itemFound = self.linearSearch(primary['mac'],list_mac)
            if itemFound:
                    log.log(log.LOG_ERROR,"host mac: {0} is already set,duplication is not allowed".format(primary['mac']))
                    sys.exit(1)
            
            list_ip.append(primary['ip'])
            list_mac.append(primary['mac'])
            


    def validate_config_psystem(self):
        log.log(log.LOG_INFO, "Validate Partition System")
        ptable_system=self.get_config_section('partition_system')
        try:
            self.validator.ptable_system(ptable_system)
        except MultipleInvalid as e:
            log.log(log.LOG_ERROR, "Cannot create partition system '{0}': \n YAML validation Error: {1}".format(ptable_system, e))
            sys.exit(1)

