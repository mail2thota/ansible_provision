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
        self.config = config['foreman']
        self.config_glb = config
        self.validator = Validator()
       
    def validate_main_yml(self):
        log.log(log.LOG_INFO, "Validate Foreman Main YML")
        try:
           validyml='foreman'
           if type(self.config_glb[validyml]) is not dict:
               raise
           validyml='auth'
           if type(self.config[validyml]) is not dict:
               raise
           validyml='domain'
           if type(self.config[validyml][0]) is not dict:
               raise
           validyml='subnet'
           if type(self.config[validyml][0]) is not dict:
               raise
           validyml='hostgroup'
           if type(self.config[validyml][0]) is not dict:
               raise
           validyml='primary_hosts'
           if type(self.config[validyml][0]) is not dict:
               raise
           validyml='secondary_hosts'
           self.ifexist=False
           if validyml in self.config:
               self.ifexist=True
               if type(self.config[validyml][0]) is not dict:
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
           validyml='primary_interface'
           if type(self.config[validyml]) is not dict:
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
        for arch in self.get_config_section('architecture'):
            try:
                self.validator.arch(arch)
            except MultipleInvalid as e:
                log.log(log.LOG_ERROR, "Cannot create Architecture '{0}' \n YAML validation Error: {1}".format(arch, e))
                sys.exit(1)


    def validate_config_domain(self):
        log.log(log.LOG_INFO, "Validate Domains")
        for domain in self.get_config_section('domain'):
            try:
                self.validator.domain(domain)
            except MultipleInvalid as e:
                log.log(log.LOG_ERROR, "Cannot create Domain '{0}' \n YAML validation Error: {1}".format(domain, e))
                sys.exit(1)


    def validate_config_medium(self):
        log.log(log.LOG_INFO, "Validate Media")
        for medium in self.get_config_section('medium'):
            try:
                self.validator.medium(medium)
            except MultipleInvalid as e:
                log.log(log.LOG_ERROR, "Cannot create Media '{0}': \n YAML validation Error: {1}".format(medium, e))
                sys.exit(1)
            

    def validate_config_settings(self):
        log.log(log.LOG_INFO, "Validate Foreman Settings")
        for setting in self.get_config_section('setting'):
            try:
                self.validator.setting(setting)
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
        for items in self.get_config_section(section):
             if items['name'] == name:
                 return True 
        
        log.log(log.LOG_ERROR, "'{0}'was not found in the list of YAML section: '{1}'".format(name,section))
        sys.exit(1)

 
    def validate_config_subnet(self):
        log.log(log.LOG_INFO, "Validate Subnets")
        for subnet in self.get_config_section('subnet'):
            try:
                self.validator.subnet(subnet)
            except MultipleInvalid as e:
                log.log(log.LOG_ERROR, "Cannot create Subnet '{0}': \n YAML validation Error: {1}".format(subnet, e))
                sys.exit(1)
            for domain in subnet['domain']:
                dname=domain['name']
                self.validate_mutual_exclusive('domain',dname)
 

    def validate_config_os(self):
        log.log(log.LOG_INFO, "Validate Operating Systems")
        for operatingsystem in self.get_config_section('os'):
            try:
                self.validator.os(operatingsystem)
            except MultipleInvalid as e:
                log.log(log.LOG_ERROR, "Cannot create Operating System '{0}': \n YAML validation Error: {1}".format(operatingsystem, e))
                sys.exit(1)
            for arches in operatingsystem['architecture']:
                archname=arches['name']
                self.validate_mutual_exclusive('architecture',archname)

            for medias in operatingsystem['medium']:
                mdname=medias['name']
                self.validate_mutual_exclusive('medium',mdname)



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
        for hostgroup in self.get_config_section('hostgroup'):
            try:
                self.validator.hostgroup(hostgroup)
            except MultipleInvalid as e:
                log.log(log.LOG_ERROR, "Cannot create Hostgroup '{0}': \n YAML validation Error: {1}".format(hostgroup, e))
                sys.exit(1)
            
            sbname=hostgroup['subnet']
            self.validate_mutual_exclusive('subnet',sbname)
            dname=hostgroup['domain']
            self.validate_mutual_exclusive('domain',dname)

    def validate_identifier(self):
        log.log(log.LOG_INFO, "Validate Primary Network Interface Identifier")
        identifier=self.get_config_section('primary_interface')
        try:
            self.validator.primary_interface(identifier) 
        except MultipleInvalid as e:
            log.log(log.LOG_ERROR, "Cannot create primary interface '{0}': \n YAML validation Error: {1}".format(identifier, e))
            sys.exit(1)

    def load_config_primaryhosts(self):
        log.log(log.LOG_INFO, "Validate Primary Hosts")
        for hostc in self.get_config_section('primary_hosts'):
            try:
                self.validator.primary_hosts(hostc)
            except MultipleInvalid as e :
                log.log(log.LOG_ERROR, "Cannot create primary hosts '{0}': \n YAML validation Error: {1}".format(hostc, e))
                sys.exit(1)
            hgname=hostc['hostgroup']
            self.validate_mutual_exclusive('hostgroup',hgname)

    def load_config_secondaryhosts(self):
        if self.ifexist:
            log.log(log.LOG_INFO, "Validate Secondary Hosts")
            for hostc in self.get_config_section('secondary_hosts'):
                try:
                    self.validator.secondary_hosts(hostc)
                except MultipleInvalid as e :
                    log.log(log.LOG_ERROR, "Cannot create secondary hosts '{0}': \n YAML validation Error: {1}".format(hostc, e))
                    sys.exit(1)
                sbname=hostc['subnet']
                self.validate_mutual_exclusive('subnet',sbname)
                hostname=hostc['primary']
                self.validate_mutual_exclusive('primary_hosts',hostname)


