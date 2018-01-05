#!/usr/bin/python
# -*- coding: utf8 -*-
#Copyright:@BaeSystemsAI
#Original author: Heri Sutrisno
#Email:harry.sutrisno@baesystems.com
#Description: main project


import yaml
import sys
import os
import log
import logging
import shutil
from payload import ForemanLoad

def fm_import(fm_impt):
  
     # main_yml
    fm_impt.validate_main_yml()

    # auth
    fm_impt.validate_auth()

    # ptable_system
    fm_impt.validate_config_psystem()
    
    # ptable
    fm_impt.validate_config_ptable()
 
    # architecture
    fm_impt.validate_config_arch()

    # domain
    fm_impt.validate_config_domain()

    # medium
    fm_impt.validate_config_medium()

    # foreman specific settings
    fm_impt.validate_config_settings()
   
    # protocol
    fm_impt.validate_protocol()

    #smartproxy
    fm_impt.validate_config_smartproxy()

    #global templates
    #fm_impt.load_config_template()

    # subnet
    fm_impt.validate_config_subnet()

    # operating system
    fm_impt.validate_config_os()

    # hostgroup
    fm_impt.validate_config_hostgroup()

    # primary host
    fm_impt.load_config_primaryhosts()

    # secondary host
    fm_impt.load_config_secondaryhosts()

    # ip and mac address validation
    fm_impt.validate_ipmac()
    
    log.log(log.LOG_INFO, "Validation Process Has Finished")

def mergeYAML(usercfg, systemcfg):
    if isinstance(usercfg,dict) and isinstance(systemcfg,dict):
        for k,v in systemcfg.iteritems():
            if k not in usercfg:
                usercfg[k] = v
            else:
                usercfg[k] = mergeYAML(usercfg[k],v)

    return usercfg


def main():
    try:
        action = sys.argv[1]
    except:
        log.log(log.LOG_ERROR, "No action defined")
        log.log(log.LOG_ERROR,"Valid: import /path/filename.yml /path/system.yml")
        sys.exit(1)

    if os.path.isfile(sys.argv[1]):
        config_file = sys.argv[1]
        cfg_path = sys.argv[2]
        action = "import"
    else:
        try:
            config_file = sys.argv[2]
            cfg_path = sys.argv[3]
        except IndexError:
            log.log(log.LOG_ERROR, "No YAML provided")
            log.log(log.LOG_ERROR,"pass argument import /path/filename.yml /path/system.yml")
            sys.exit(1)
    
    try:
        config_file = open(config_file, 'r')
        try:
            config = yaml.load(config_file)
        except yaml.YAMLError, exc:
            log.log(log.LOG_ERROR, "Failed to load/parse import config YAML, Error:'{0}'".format(exc))
            log.log(log.LOG_INFO, "Check if '{0}' is formatted correctly".format(config_file))
            sys.exit(1)
        config_file.close()
    except IOError as e:
        log.log(log.LOG_ERROR, "Failed to open/load import config YAML Error:'{0}'".format(e))
        log.log(log.LOG_INFO, "Check if '{0}' is available".format(config_file))
        sys.exit(1)

    try:
        config_default_file = open(cfg_path, 'r')
        try:
            config_default = yaml.load(config_default_file)
        except yaml.YAMLError, exc:
            log.log(log.LOG_ERROR, "Failed to load/parse system config YAML, Error:'{0}'".format(exc))
            log.log(log.LOG_INFO, "Check if '{0}' formatted correctly".format(cfg_path))
            sys.exit(1)
        config_default_file.close()
        config = mergeYAML(config, config_default)
        
    except IOError as e:
        log.log(log.LOG_ERROR, "Failed to open/load system config YAML Error:'{0}'".format(e))
        log.log(log.LOG_INFO, "Check if '{0}' is available".format(cfg_path))
        sys.exit(1)

    if (action == "import"):
        fm_impt = ForemanLoad(config)
        fm_import(fm_impt)

if __name__ == '__main__':
    main()