#!/usr/bin/python
# -*- coding: utf8 -*-
#Copyright:@BaeSystemsAI
#Original author: Heri Sutrisno
#Email:harry.sutrisno@baesystems.com
#Description:validation schema

from voluptuous import Schema, Required, All, Length, Optional, Any, Match


class Validator:

    def __init__(self):
          
        self.auth = Schema({
            Required('foreman_fqdn'):                   Match("^[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$", msg='must be valid fqdn ex:bootstrap.example.com'),
            Required('foreman_ip'):                     Match("^(?:(?:^|\.)(?:2(?:5[0-5]|[0-4]\d)|1?\d?\d)){4}$",msg='must be valid ipv4 ex:10.11.12.23'),
        })


        self.arch = Schema({
            Required('name'):                           All(str, msg='support x86_64 only'),
        })

        self.protocol = Schema({
            Required('type'):                           Any('http',msg='support http protocol only'),
        })

        self.foreman_proxy = Schema({
            Required('port'):                           All(int,msg='port number must be in digit'),
        })

        self.domain = Schema({
            Required('name'):                           Match("^[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$", msg='must be valid domain ex:domain-name.com'),
            Optional('fullname'):                       Any(str, None)
        })

        self.medium = Schema({
            Required('name'):                           All(str, msg='medium name'),
            Required('path'):                           All(str, msg='repository path for centos image ex:/repos/CentOS_7_x86_64/'),
            Required('os_family'):                      All(str, msg='\'os_family\' ex: Redhat'),
        })

        self.ptable = Schema({
            Required('name'):                           All(str),

            Required('boot'):                           Any(Schema({
                Required('fstype'):                     Any('xfs','ext2','ext3','ext4',msg='support \'xfs,ext2,ext3,ext4\''),                                          
                Required('size'):                       All(int,msg='size in percentage'),
            })),

            Required('swap'):                           Any(Schema({
                Required('fstype'):                     Any('swap',msg='support swap'),
                Required('size'):                       All(int,msg='size in percentage'),
            })),

            Required('tmp'):                            Any(Schema({
                Required('fstype'):                     Any('xfs','ext2','ext3','ext4',msg='support \'xfs,ext2,ext3,ext4\''),                                          
                Required('size'):                       All(int,msg='size in percentage'),
            })),

            Required('var'):                            Any(Schema({
                Required('fstype'):                     Any('xfs','ext2','ext3','ext4',msg='support \'xfs,ext2,ext3,ext4\''),                                          
                Required('size'):                       All(int,msg='size in percentage'),
            })),

            Required('home'):                           Any(Schema({
                Required('fstype'):                     Any('xfs','ext2','ext3','ext4',msg='support \'xfs,ext2,ext3,ext4\''),                                          
                Required('size'):                       All(int,msg='size in percentage'),
            })),

            Required('root'):                           Any(Schema({
                Required('fstype'):                     Any('xfs','ext2','ext3','ext4',msg='support \'xfs,ext2,ext3,ext4\''),                                          
                Required('size'):                       All(int,msg='size in percentage'),
            })),
        })


        self.ptable_system = Schema({
            Required('disk_minimum'):                    All(int,msg='size in gigabyte format, max default disk size'),
            Required('boot_size'):                       Any(int,msg='size in megabyte format'),
            Required('boot_type'):                       Any('xfs','ext2','ext3','ext4',msg='support \'xfs,ext2,ext3,ext4\''),
            Required('swap_size'):                       All(int,msg='size in megabyte format'),
            Required('swap_type'):                       Any('swap',msg='support swap only'),
            Required('home_size'):                       All(int,msg='size in megabyte format'),
            Required('home_type'):                       Any('xfs','ext2','ext3','ext4',msg='support \'xfs,ext2,ext3,ext4\''),
            Required('var_size'):                        All(int,msg='size in megabyte format'),
            Required('var_type'):                        Any('xfs','ext2','ext3','ext4',msg='support \'fs,ext2,ext3,ext4\''),
            Required('tmp_size'):                        All(int,msg='size in megabyte format'),
            Required('tmp_type'):                        Any('xfs','ext2','ext3','ext4',msg='support \'xfs,ext2,ext3,ext4\''),
            Required('root_size'):                       All(int,msg='size in megabyte format'),
            Required('root_type'):                       Any('xfs','ext2','ext3','ext4',msg='support \'fs,ext2,ext3,ext4\''),
  
        })

        self.os = Schema({
            Required('name'):                           All(str, msg='name for os ex: CentOS7'),
            Required('family'):                         Any(str, msg='os family ex: Redhat'),
            Required('password_hash'):                  Any(
                                                            'MD5',
                                                            'SHA256',
                                                            'SHA512',
                                                            'Base64',
                                                            msg='only support SHA512'
                                                            ),
            Required('architecture'):                   Any(Schema([{
                Required('name'):                       All(str,msg='only support x86_64')
            }])),
            Required('provisioning_template'):          Any(Schema([{
                Required('name'):                       All(str, msg='support Kickstarter template')
            }])),
            Required('medium'):                         Any(Schema([{
                Required('name'):                       All(str,msg='assigned medium name')
            }])),
        })

        self.primary_hosts = Schema({
            Required('name'):                           All(str,msg='required valid hostname'),
            Required('hostgroup'):                      Any(str,msg='assigned hostgroup name'),
            Required('ip'):                             Match("^(?:(?:^|\.)(?:2(?:5[0-5]|[0-4]\d)|1?\d?\d)){4}$",msg='provide valid ipv4'), 
            Required('mac'):                            Match("^[a-fA-F0-9:]{17}|[a-fA-F0-9]{12}$",msg='provide valid mac address'),
            Optional('tags'):                           Any(list,msg='required list of tags')
        })

        self.secondary_hosts = Schema({
            Required('ip'):                             Match("^(?:(?:^|\.)(?:2(?:5[0-5]|[0-4]\d)|1?\d?\d)){4}$",msg='provide valid ipv4'), 
            Required('mac'):                            Match("^[a-fA-F0-9:]{17}|[a-fA-F0-9]{12}$",msg='provide valid mac address'),
            Required('subnet'):                         Any(str,msg='provide valid subnet ipv4'),
            Required('primary'):                        All(str,msg='required valid primary hostname'),

        })

        self.hostgroup = Schema({
            Required('name'):                           All(str,msg='provide hostgroup name'),
            Required('subnet'):                         Any(str,msg='provide valid subnet ipv4'),
            Required('domain'):                         Any(str,msg='assigned valid domain'),
            Required('partition_table'):                Any(str,msg='assigned valid partition table'),
        })

        self.hostgroup_system = Schema({
            Required('os'):                             Any(str,msg='assigned os name'),
            Required('architecture'):                   Any(str,msg='assigned architecture name'),
            Required('medium'):                         Any(str,msg='assigned medium name'),
        })

        self.primary_interface = Schema({
            Required('identifier'):                     All(str,msg='primary network interface identifier ex: enp0s3,eth0,eth1'),
        })

        self.setting = Schema({
            Required('name'):                           All(str,msg='valid setting name'),
            Required('value'):                          Any(list, str, bool,
                                                            int, None),
        })

        self.subnet =  Schema({
            Required('name'):                           All(str,msg='name for subnet is required'),
            Required('network'):                        Match("^(?:(?:^|\.)(?:2(?:5[0-5]|[0-4]\d)|1?\d?\d)){4}$",msg='valid ipv4 for subnet is required'),
            Required('mask'):                           Match("^(?:(?:^|\.)(?:2(?:5[0-5]|[0-4]\d)|1?\d?\d)){4}$",msg='valid ipv4 for mask is required'),
            Optional('gateway'):                        Any(str, None),
            Optional('dns_primary'):                    Any(str, None),
            Optional('dns_secondary'):                  Any(str, None),
            Optional('ipam'):                           Any('DHCP', 'Internal DB', 'None', None),
            Optional('vlanid'):                         Any(str, int, None),
            Required('domain'):                         Any(Schema([{
                Required('name'):                       Match("^[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$",msg='assigned domain name')
            }])),

        })
