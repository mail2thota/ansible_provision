#!/usr/bin/python
# -*- coding: utf8 -*-
#Copyright:@BaeSystemsAI
#Original author: Heri Sutrisno
#Email:harry.sutrisno@baesystems.com
#Description:clenup resources

import log
import json
from foreman_base import ForemanBase
from voluptuous import MultipleInvalid


class ForemanCleanup(ForemanBase):

    def cleanup_global_params(self):
        log.log(log.LOG_INFO, "Processing Cleanup of global parameter")
        try:
            json_buff = self.fm.common_parameters.index()['results']
            json_str = json.dumps(json_buff)
            json_dicts = json.loads(json_str)
            log.log(log.LOG_INFO, "Delete global parameter")
            for each in json_dicts:
                log.log(log.LOG_INFO, "remove parameter: '{0}' id '{1}'".format(each['name'],each['id']))
                self.fm.common_parameters.destroy(each['id'])
        except:
            log.log(log.LOG_WARN, "global parameter already absent from list")

    def cleanup_hosts(self):
        log.log(log.LOG_INFO, "Processing Cleanup of hosts")
        try:
            json_buff = self.fm.hosts.index()['results']
            json_str = json.dumps(json_buff)
            json_dicts = json.loads(json_str)
            log.log(log.LOG_INFO, "Delete hosts")
            for each in json_dicts:
                log.log(log.LOG_INFO, "remove host: '{0}' id '{1}'".format(each['name'],each['id']))
                self.fm.hosts.destroy(each['id'])
        except:
            log.log(log.LOG_WARN, "host already absent from list")

    def cleanup_hostgroups(self):
        log.log(log.LOG_INFO, "Processing Cleanup of hostgroups")
        try:
            json_buff = self.fm.hostgroups.index()['results']
            json_str = json.dumps(json_buff)
            json_dicts = json.loads(json_str)
            log.log(log.LOG_INFO, "Delete hostgroups")
            for each in json_dicts:
                log.log(log.LOG_INFO, "remove hostgroups: '{0}' id '{1}'".format(each['name'],each['id']))
                self.fm.hostgroups.destroy(each['id'])
        except:
            log.log(log.LOG_WARN, "hostgroups already absent from list")

    def cleanup_subnets(self):
        log.log(log.LOG_INFO, "Processing Cleanup of subnets")
        try:
            json_buff = self.fm.subnets.index()['results']
            json_str = json.dumps(json_buff)
            json_dicts = json.loads(json_str)
            log.log(log.LOG_INFO, "Delete subnets")
            for each in json_dicts:
                log.log(log.LOG_INFO, "remove subnets: '{0}' id '{1}'".format(each['name'],each['id']))
                self.fm.subnets.update(id=each['id'], subnet={'domains':[{'id':None}]})
                self.fm.subnets.destroy(each['id'])
        except:
            log.log(log.LOG_WARN, "subnets already absent from list")

    def cleanup_domains(self):
        log.log(log.LOG_INFO, "Processing Cleanup of domains")
        try:
            json_buff = self.fm.domains.index()['results']
            json_str = json.dumps(json_buff)
            json_dicts = json.loads(json_str)
            log.log(log.LOG_INFO, "Delete domains")
            for each in json_dicts:
                log.log(log.LOG_INFO, "remove domains: '{0}' id '{1}'".format(each['name'],each['id']))
                self.fm.domains.destroy(each['id'])
        except:
            log.log(log.LOG_WARN, "domains already absent from list")
