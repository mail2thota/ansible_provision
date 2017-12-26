#!/usr/bin/python
# -*- coding: utf8 -*-
#Copyright:@BaeSystemsAI
#Original author: Heri Sutrisno
#Email:harry.sutrisno@baesystems.com
#Description: base class for foreman-python

import sys
import logging
import log
import socket
import urllib3
from foreman.client import Foreman


class ForemanBase:

    def __init__(self, config, loglevel=logging.INFO):
        logging.basicConfig(level=loglevel)
        log.LOGLEVEL = loglevel
        self.config = config['foreman']
        self.common =  config['common']
        self.loglevel = loglevel

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

    def check_secondary_host(self):
        log.log(log.LOG_INFO, "Check Secondary Host")
        try:
            validyml='secondary_hosts'
            self.ifexist=False
            if validyml in self.config:
                self.ifexist=True
                if type(self.config[validyml][0]) is not dict:
                    raise
        except:
            log.log(log.LOG_ERROR, "Section '{0}' is required: YAML validation Error".format(validyml))
            log.log(log.LOG_ERROR, "Section '{0}' type unknown, it must be key and value: YAML validation Error".format(validyml))
            sys.exit(1)

    def get_protocol(self):
        setting_sect = self.get_config_section('protocol')            
        protocol = setting_sect['type']
        return protocol
        
    def get_fm_hostname(self):
        authsection = self.get_config_section('auth')
        fmhostname = authsection['foreman_fqdn'] 
        return fmhostname

    def get_fm_ip(self):
        authsection = self.get_config_section('auth')
        fmip = authsection['foreman_ip']
        fmprotocolip = "{0}://".format(self.get_protocol())
        #fmfqdn = fmprotocolip+self.get_fm_hostname()
        fmprotocolip += fmip
        return fmprotocolip

    def set_repo_ip(self, ip):
        self.repo_ip = ip

    def get_repo_ip(self):
        return self.repo_ip          
 
    def connect(self):
        log.log(log.LOG_INFO, "Establish connection to Foreman server")
        fm_ip = self.get_fm_ip()
        try:
            logging.disable(logging.WARNING)
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            authsection = self.get_config_section('auth')
            self.fm = Foreman(fm_ip, (authsection['foreman_user'], authsection['foreman_pass']), api_version=2, use_cache=False, strict_cache=False)
            # this is nescesary for detecting faulty credentials in yaml
            self.fm.architectures.index()
            logging.disable(self.loglevel-1)
            log.log(log.LOG_INFO, "Establish connection to Foreman server succeeded")
        except:
            log.log(log.LOG_ERROR, "Cannot connect to Foreman-API")
            sys.exit(1)

    def get_api_error_msg(self, e):
        dr = e.res.json()
        try:
            msg = dr['error']['message']
        except KeyError:
            msg = dr['error']['full_messages'][0]

        return msg


