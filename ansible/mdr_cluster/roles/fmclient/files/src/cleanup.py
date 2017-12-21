#!/usr/bin/python
# -*- coding: utf8 -*-
#Copyright:@BaeSystemsAI
#Original author: Heri Sutrisno
#Email:harry.sutrisno@baesystems.com
#Description:clenup resources

import sys
import log
import json
from foreman_base import ForemanBase


class ForemanCleanup(ForemanBase):

    def cleanup_global_params(self):
        log.log(log.LOG_INFO, "Processing Cleanup of global parameter")
        try:
            json_buff = self.fm.common_parameters.index()['results']
            if not json_buff:
                return log.log(log.LOG_WARN, "global parameter already absent from list")
            json_str = json.dumps(json_buff)
            json_dicts = json.loads(json_str)
            log.log(log.LOG_INFO, "Delete global parameter")
            for each in json_dicts:
                log.log(log.LOG_INFO, "remove parameter: '{0}' id '{1}'".format(each['name'],each['id']))
                self.fm.common_parameters.destroy(each['id'])
        except:
            log.log(log.LOG_ERROR, "can not be removed '{0}' id '{1}', check your config".format(each['name'],each['id']))
            sys.exit(1)

    def cleanup_hosts(self):
        log.log(log.LOG_INFO, "Processing Cleanup of hosts")
        try:
            json_buff = self.fm.hosts.index()['results']
            if not json_buff:
                return log.log(log.LOG_WARN, "host already absent from list")
            json_str = json.dumps(json_buff)
            json_dicts = json.loads(json_str)
            log.log(log.LOG_INFO, "Delete hosts")
            for each in json_dicts:
                log.log(log.LOG_INFO, "remove host: '{0}' id '{1}'".format(each['name'],each['id']))
                log_remove = self.fm.hosts.destroy(each['id'])
        except:
            log.log(log.LOG_ERROR, "can not be removed '{0}' id '{1}', check your foreman-proxy config".format(each['name'],each['id']))
            sys.exit(1)

    def cleanup_hostgroups(self):
        log.log(log.LOG_INFO, "Processing Cleanup of hostgroups")
        try:
            json_buff = self.fm.hostgroups.index()['results']
            if not json_buff:
                return log.log(log.LOG_WARN, "hostgroups already absent from list")
            json_str = json.dumps(json_buff)
            json_dicts = json.loads(json_str)
            log.log(log.LOG_INFO, "Delete hostgroups")
            for each in json_dicts:
                log.log(log.LOG_INFO, "remove hostgroups: '{0}' id '{1}'".format(each['name'],each['id']))
                self.fm.hostgroups.destroy(each['id'])
        except:
            log.log(log.LOG_ERROR, "can not be removed '{0}' id '{1}', check your subnet and domain dependencies".format(each['name'],each['id']))
            sys.exit(1)

    def cleanup_subnets(self):
        log.log(log.LOG_INFO, "Processing Cleanup of subnets")
        try:
            json_buff = self.fm.subnets.index()['results']
            if not json_buff:
                return log.log(log.LOG_WARN, "subnets already absent from list")
            json_str = json.dumps(json_buff)
            json_dicts = json.loads(json_str)
            log.log(log.LOG_INFO, "Delete subnets")
            for each in json_dicts:
                log.log(log.LOG_INFO, "remove subnets: '{0}' id '{1}'".format(each['name'],each['id']))
                self.fm.subnets.update(id=each['id'], subnet={'domains':[{'id':None}]})
                self.fm.subnets.destroy(each['id'])
        except:
            log.log(log.LOG_ERROR, "can not be removed '{0}' id '{1}', check your domain dependencies".format(each['name'],each['id']))
            sys.exit(1)


    def cleanup_domains(self):
        log.log(log.LOG_INFO, "Processing Cleanup of domains")
        try:
            json_buff = self.fm.domains.index()['results']
            if not json_buff:
                return log.log(log.LOG_WARN, "domains already absent from list")
            json_str = json.dumps(json_buff)
            json_dicts = json.loads(json_str)
            log.log(log.LOG_INFO, "Delete domains")
            for each in json_dicts:
                log.log(log.LOG_INFO, "remove domains: '{0}' id '{1}'".format(each['name'],each['id']))
                self.fm.domains.destroy(each['id'])
        except:
            log.log(log.LOG_ERROR, "can not be removed '{0}' id '{1}', check your subnet dependencies".format(each['name'],each['id']))
            sys.exit(1)

    def cleanup_smart_proxy(self):
        log.log(log.LOG_INFO, "Processing Cleanup of smart_proxy")
        try:
            json_buff = self.fm.smart_proxies.index()['results']
            if not json_buff:
                return log.log(log.LOG_WARN, "smart proxy already absent from list")
            json_str = json.dumps(json_buff)
            json_dicts = json.loads(json_str)
            log.log(log.LOG_INFO, "Delete smart proxy")
            for each in json_dicts:
                log.log(log.LOG_INFO, "remove smart proxy: '{0}' id '{1}'".format(each['name'],each['id']))
                self.fm.smart_proxies.destroy(each['id'])
        except:
            log.log(log.LOG_ERROR, "can not be removed '{0}' id '{1}', check your foreman-proxy config file".format(each['name'],each['id']))
            sys.exit(1)


    def cleanup_ptable(self):
        log.log(log.LOG_INFO, "Processing Cleanup of partition table")
        try:
            json_buff = self.fm.ptables.index()['results']
            if not json_buff:
                return log.log(log.LOG_WARN, "patition table already absent from list")
            json_str = json.dumps(json_buff)
            json_dicts = json.loads(json_str)
            log.log(log.LOG_INFO, "Delete partition table")
            for each in json_dicts:
                log.log(log.LOG_INFO, "remove partition table: '{0}' id '{1}'".format(each['name'],each['id']))
                self.fm.ptables.destroy(each['id'])
        except:
            log.log(log.LOG_ERROR, "can not be removed '{0}' id '{1}', check your partition table YML config file".format(each['name'],each['id']))
            sys.exit(1)

    def cleanup_os(self):
         log.log(log.LOG_INFO, "Processing Cleanup of operating systems")
         try:
             json_buff = self.fm.operatingsystems.index()['results']
             if not json_buff:
                 return log.log(log.LOG_WARN, "operating system already absent from list")
             json_str = json.dumps(json_buff)
             json_dicts = json.loads(json_str)
             log.log(log.LOG_INFO, "Delete operating systems")
             for each in json_dicts:
                 log.log(log.LOG_INFO, "remove operating system: '{0}' id '{1}'".format(each['name'],each['id']))
                 self.fm.operatingsystems.destroy(each['id'])
         except:
             log.log(log.LOG_ERROR, "can not be removed '{0}' id '{1}', check your operating system YML config file".format(each['name'],each['id']))
             sys.exit(1)


    def cleanup_media(self):
         log.log(log.LOG_INFO, "Processing Cleanup of Medium")
         try:
             json_buff = self.fm.media.index()['results']
             if not json_buff:
                 return log.log(log.LOG_WARN, "mediums already absent from list")
             json_str = json.dumps(json_buff)
             json_dicts = json.loads(json_str)
             log.log(log.LOG_INFO, "Delete mediums")
             for each in json_dicts:
                 log.log(log.LOG_INFO, "remove mediums: '{0}' id '{1}'".format(each['name'],each['id']))
                 self.fm.media.destroy(each['id'])
         except:
             log.log(log.LOG_ERROR, "can not be removed '{0}' id '{1}', check your mediums YML config file".format(each['name'],each['id']))
             sys.exit(1)

    def cleanup_arch(self):
         log.log(log.LOG_INFO, "Processing Cleanup of Architectures")
         try:
             json_buff = self.fm.architectures.index()['results']
             if not json_buff:
                 return log.log(log.LOG_WARN, "architecture already absent from list")
             json_str = json.dumps(json_buff)
             json_dicts = json.loads(json_str)
             log.log(log.LOG_INFO, "Delete architectures")
             for each in json_dicts:
                 log.log(log.LOG_INFO, "remove architectures: '{0}' id '{1}'".format(each['name'],each['id']))
                 self.fm.architectures.destroy(each['id'])
         except:
             log.log(log.LOG_ERROR, "can not be removed '{0}' id '{1}', check your architectures YML config file".format(each['name'],each['id']))
             sys.exit(1)

