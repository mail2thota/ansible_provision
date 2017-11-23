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
from cleanup import ForemanCleanup


cfg_path='/opt/foreman_yml/.system.yml'

def fm_cleanup(fm_clean):
    #cleanup global parameters
    fm_clean.cleanup_global_params()

    #clean up hosts
    fm_clean.cleanup_hosts()

    #cleanup hostgroups
    fm_clean.cleanup_hostgroups()

    #cleanup subnets
    fm_clean.cleanup_subnets()

   #cleanup domain
    fm_clean.cleanup_domains()

def mergeYAML(usercfg, systemcfg):
    if isinstance(usercfg,dict) and isinstance(systemcfg,dict):
        for k,v in systemcfg.iteritems():
            if k not in usercfg:
                usercfg[k] = v
            else:
                usercfg[k] = mergeYAML(usercfg[k],v)

    return usercfg

def fm_import(fm_impt):
    # global params
    fm_impt.load_global_params()

    # internal settings
    fm_impt.load_foremanurl_settings()

    # global settings
    fm_impt.load_config_settings()
    
    # architecture
    fm_impt.load_config_arch()

    # domain
    fm_impt.load_config_domain()

    # medium
    fm_impt.load_config_medium()

    #smartproxy
    fm_impt.load_config_smartproxy()

    #global templates
    fm_impt.load_config_template()

    # subnet
    fm_impt.load_config_subnet()

    # operating system
    fm_impt.load_config_os()

    # Link items to operating system
    fm_impt.load_config_os_link()

    # hostgroup
    fm_impt.load_config_hostgroup()

    # host
    fm_impt.load_config_host()

def main():
    try:
        action = sys.argv[1]
    except:
        log.log(log.LOG_ERROR, "No action defined (Valid: import /path/filename.yml)")
        sys.exit(1)

    if sys.argv[1] != 'import':
       log.log(log.LOG_ERROR, "No valid action (Valid: import /path/filename.yml)")
       sys.exit(1)

    if os.path.isfile(sys.argv[1]):
        config_file = sys.argv[1]
        action = "import"
    else:
        try:
            config_file = sys.argv[2]
        except IndexError:
            log.log(log.LOG_ERROR, "No YAML provided")
            sys.exit(1)

    try:
        config_file = open(config_file, 'r')
        try:
            config = yaml.load(config_file)
        except yaml.YAMLError, exc:
            log.log(log.LOG_ERROR, "Failed to load/parse import config YAML, Error:'{0}'".format(exc))
            log.log(log.LOG_INFO, "Check if '{0}' formatted correctly".format(config_file))
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
        config_default_file.close()

        config = mergeYAML(config, config_default)
    except IOError as e:
        log.log(log.LOG_ERROR, "Failed to open/load system config YAML Error:'{0}'".format(e))
        log.log(log.LOG_INFO, "Check if '{0}' is available".format(cfg_path))
        sys.exit(1)

    if (action == "import"):
        fm_clean = ForemanCleanup(config)
        fm_clean.connect()
        fm_cleanup(fm_clean)
        fm_impt = ForemanLoad(config)
        fm_impt.connect()
        fm_import(fm_impt)

if __name__ == '__main__':
    main()
