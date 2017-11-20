#!/usr/bin/python
# -*- coding: utf8 -*-
#Copyright:@BaeSystemsAI
#Original author: Heri Sutrisno
#Email:harry.sutrisno@baesystems.com
#Description:validation schema

from voluptuous import Schema, Required, All, Length, Optional, Any


class Validator:

    def __init__(self):

        self.arch = Schema({
            Required('name'):                           All(str),
        })

        self.domain = Schema({
            Required('name'):                           All(str),
            Optional('fullname'):                       Any(str, None)
        })

        self.medium = Schema({
            Required('name'):                           All(str),
            Required('path'):                           All(str),
            Required('os_family'):                      All(str),
        })

        self.ptable = Schema({
            Required('name'):                           All(str),
            Required('layout'):                         All(str),
            Optional('snippet'):                        Any(bool,None),
            Optional('os_family'):                      Any(str,None),
            Optional('audit_comment'):                  Any(str,None),
            Optional('locked'):                         Any(bool,None),
        })

        self.os = Schema({
            Required('name'):                           All(str),
            Required('major'):                          Any(str, int),
            Required('minor'):                          Any(str, int),
            Optional('description'):                    Any(str, None),
            Optional('family'):                         Any(str, None),
            Optional('release_name'):                   Any(str, None),
            Optional('parameters'):                     Any(dict, None),
            Optional('password_hash'):                  Any(
                                                            'MD5',
                                                            'SHA256',
                                                            'SHA512',
                                                            'Base64',
                                                            None
                                                            ),
            Optional('architecture'):                   Any(None, Schema([{
                Required('name'):                       All(str)
            }])),
            Optional('provisioning_template'):          Any(None, Schema([{
                Required('name'):                       All(str)
            }])),
            Optional('medium'):                         Any(None, Schema([{
                Required('name'):                       All(str)
            }])),
            Optional('partition_table'):                Any(None, Schema([{
                Required('name'):                       All(str)
            }]))
        })

        self.host = Schema({
            Required('name'):                           All(str),
            Required('hostgroup'):                      Any(str),
            Required('ip'):                             Any(str),
            Required('mac'):                            Any(str),
        })

        self.hostgroup = Schema({
            Required('name'):                           All(str),
            Required('subnet'):                         Any(str),
            Required('domain'):                         Any(str),
            Required('root_pass'):                      All(str, Length(min=8)),

        })

        self.hostgroup_default = Schema({
            Required('name'):                           All(str),
            Optional('parent'):                         Any(str, None),
            Required('os'):                             Any(str),
            Required('architecture'):                   Any(str),
            Required('medium'):                         Any(str),
            Required('partition_table'):                Any(str),

        })

        self.setting = Schema({
            Required('name'):                           All(str),
            Optional('value'):                          Any(list, str, bool,
                                                            int, None),
            Required('protocol'):                       Any('http', 'https'),

        })

        self.subnet =  Schema({
            Required('name'):                           All(str),
            Required('network'):                        All(str),
            Required('mask'):                           All(str),
            Optional('gateway'):                        Any(str, None),
            Optional('dns_primary'):                    Any(str, None),
            Optional('dns_secondary'):                  Any(str, None),
            Optional('ipam'):                           Any('DHCP', 'Internal DB', 'None', None),
            Optional('vlanid'):                         Any(str, int, None),
            Required('domain'):                         Any(None, Schema([{
                Required('name'):                       All(str)
            }])),

        })
