#!/usr/bin/python
# -*- coding: utf8 -*-
#Copyright:@BaeSystemsAI
#Original author: Heri Sutrisno
#Email:harry.sutrisno@baesystems.com
#Description:payload foreman resources

import sys
import log
from foreman_base import ForemanBase
from pprint import pprint
from foreman.client import Foreman, ForemanException
from voluptuous import MultipleInvalid

class ForemanLoad(ForemanBase):

    def load_global_params(self):
        log.log(log.LOG_INFO, "Load global parameters")
        global_tpl = {
        'disable-firewall': 'true',
        'enable-epel': 'false',
        'enable-puppetlabs-pc1-repo': 'false',
        'enable-puppetlabs-repo': 'false',
        'package_upgrade': 'false',
        'selinux-mode': 'permissive'
        }

        for keyglobal,valglobal in global_tpl.iteritems():
            self.fm.common_parameters.create(common_parameter={'name':keyglobal, 'value':valglobal})


    def load_config_arch(self):
        log.log(log.LOG_INFO, "Load Architectures")
        for arch in self.get_config_section('architecture'):
            try:
                self.validator.arch(arch)
            except MultipleInvalid as e:
                log.log(log.LOG_ERROR, "Cannot create Architecture '{0}' \n YAML validation Error: {1}".format(arch, e))
                sys.exit(1)

            try:
                arch_id = self.fm.architectures.show(arch['name'])['id']
                log.log(log.LOG_DEBUG, "Architecture '{0}' (id={1}) already present.".format(arch, arch_id))
            except:
                log.log(log.LOG_INFO, "Create Architecture '{0}'".format(arch))
                self.fm.architectures.create( architecture = { 'name': arch['name'] } )


    def load_config_domain(self):
        log.log(log.LOG_INFO, "Load Domains")
        for domain in self.get_config_section('domain'):
            try:
                self.validator.domain(domain)
            except MultipleInvalid as e:
                log.log(log.LOG_ERROR, "Cannot create Domain '{0}' \n YAML validation Error: {1}".format(domain, e))
                sys.exit(1)
            try:
                dom_id = self.fm.domains.show(domain['name'])['id']
                log.log(log.LOG_DEBUG, "Domain '{0}' (id={1}) already present.".format(domain, dom_id))
            except:
                log.log(log.LOG_INFO, "Create Domain '{0}'".format(domain['name']))
                self.fm.domains.create(domain = {'name': domain['name'], 'fullname': domain['fullname']})



    def load_config_medium(self):
        log.log(log.LOG_INFO, "Load Media")
        medialist = self.fm.media.index(per_page=99999)['results']
        for medium in self.get_config_section('medium'):
            try:
                self.validator.medium(medium)
            except MultipleInvalid as e:
                log.log(log.LOG_ERROR, "Cannot create Media '{0}': \n YAML validation Error: {1}".format(medium, e))
                sys.exit(1)

            try:
                medium_id = self.fm.media.show(medium['name'])['id']
                log.log(log.LOG_DEBUG, "Medium '{0}' (id={1}) already present.".format(medium, medium_id))
            except:
                medium_tpl = {
                    'name':        medium['name'],
                    'path':        medium['path'],
                    'os_family':   medium['os-family']
                    }
                self.fm.media.create(medium=medium_tpl)


    def load_config_settings(self):
        log.log(log.LOG_INFO, "Load Foreman Settings")
        for setting in self.get_config_section('setting'):
            try:
                self.validator.setting(setting)
            except MultipleInvalid as e:
                log.log(log.LOG_ERROR, "Cannot update Setting '{0}': \n YAML validation Error: {1}".format(setting, e))
                sys.exit(1)
            try:
                setting_id = self.fm.settings.show(setting['name'])['id']
            except:
                log.log(log.LOG_WARN, "Cannot get ID of Setting '{0}', skipping".format(setting))

            setting_tpl = {
                'value':            setting['value'],
            }
            log.log(log.LOG_INFO, "Update Setting '{0}'".format(setting))
            self.fm.settings.update(setting_tpl, setting_id)


    def load_foremanurl_settings(self):
        log.log(log.LOG_INFO, "Load unattended and foreman url Settings")
        try:
            settingunatt_id = self.fm.settings.show('unattended_url')['id']
            settingurl_id = self.fm.settings.show('foreman_url')['id']
        except:
            log.log(log.LOG_WARN, "Cannot get ID of Setting '{0}', skipping".format('unattended_url and foreman_url'))

        settingurl_tpl = {
            'value':         self.get_fm_ip(),
        }
        log.log(log.LOG_INFO, "Update Setting unattended_url '{0}'".format('unattended_url and foreman_url'))
        self.fm.settings.update(settingurl_tpl, settingunatt_id)
        self.fm.settings.update(settingurl_tpl, settingurl_id)


    def load_config_smartproxy(self):
        log.log(log.LOG_INFO, "Load Smart Proxies")
        #simplify it on the future modification
        foreman_proxyport = ":8443"
        protocolip="https://"
        protocolip+=self.get_fm_hostname()
        foreman_proxyip = protocolip + foreman_proxyport

        try:
            proxy_id = self.fm.smart_proxies.show(self.get_fm_hostname())['id']
            log.log(log.LOG_DEBUG, "Proxy '{0}' (id={1}) already present.".format(self.get_fm_hostname(), proxy_id))
        except:
            log.log(log.LOG_INFO, "Create Smart Proxy '{0}'".format(self.get_fm_hostname()))
            proxy_tpl = {
                'name': self.get_fm_hostname(),
                'url': foreman_proxyip,
            }
            try:
                self.fm.smart_proxies.create( smart_proxy = proxy_tpl )
            except:
                log.log(log.LOG_WARN, "Cannot create Smart Proxy '{0}'. Is the Proxy online? ".format(self.get_fm_hostname()))


    def load_config_subnet(self):
        log.log(log.LOG_INFO, "Load Subnets")
        subnet_tpl_dft = {
              'dhcp-proxy': self.get_fm_hostname(),
              'tftp-proxy': self.get_fm_hostname(),
              'boot-mode' : 'Static',
              'network-type': 'IPv4',
              'dns-proxy': self.get_fm_hostname(),
              'ipam': 'None',
        }
        for subnet in self.get_config_section('subnet'):
            try:
                self.validator.subnet(subnet)
            except MultipleInvalid as e:
                log.log(log.LOG_ERROR, "Cannot create Subnet '{0}': \n YAML validation Error: {1}".format(subnet, e))
                sys.exit(1)
            try:
                subnet_id = self.fm.subnets.show(subnet['name'])['id']
                log.log(log.LOG_DEBUG, "Subnet '{0}' (id={1}) already present.".format(subnet, subnet_id))
            except:
                # get domain_ids
                add_domain = []
                for subnet_domain in subnet['domain']:
                    try:
                        dom_id = self.fm.domains.show(subnet_domain['name'])['id']
                        add_domain.append(dom_id)
                    except:
                        log.log(log.LOG_WARN, "Cannot get ID of Domain '{0}', skipping".format(subnet_domain))

                # get dhcp_proxy_id
                dhcp_proxy_id = False
                try:
                    dhcp_proxy_id = self.fm.smart_proxies.show(subnet_tpl_dft['dhcp-proxy'])['id']
                except:
                    log.log(log.LOG_WARN, "Cannot get ID of DHCP Smart Proxy '{0}', skipping".format(subnet_tpl_dft['dhcp-proxy']))

                # get tftp_proxy_id
                tftp_proxy_id = False
                try:
                    tftp_proxy_id = self.fm.smart_proxies.show(subnet_tpl_dft['tftp-proxy'])['id']
                except:
                    log.log(log.LOG_WARN, "Cannot get ID of TFTP Smart Proxy '{0}', skipping".format(subnet_tpl_dft['tftp-proxy']))


                log.log(log.LOG_INFO, "Create Subnet '{0}'".format(subnet))
                subnet_tpl = {
                    'name':             subnet['name'],
                    'network':          subnet['network'],
                    'mask':             subnet['mask'],
                    'gateway':          subnet['gateway'],
                    'dns_primary':      subnet['dns-primary'],
                    'dns_secondary':    subnet['dns-secondary'],
                    'ipam':             subnet_tpl_dft['ipam'],
                    'vlanid':           subnet['vlanid'],
                    'boot_mode':        subnet_tpl_dft['boot-mode'],
                    'network_type':     subnet_tpl_dft['network-type']
                }

                if add_domain: subnet_tpl['domain_ids'] = add_domain
                if dhcp_proxy_id: subnet_tpl['dhcp_id'] = dhcp_proxy_id
                if tftp_proxy_id: subnet_tpl['tftp_id'] = tftp_proxy_id
                self.fm.subnets.create(subnet=subnet_tpl)


    def load_config_os(self):
        log.log(log.LOG_INFO, "Load Operating Systems")
        for operatingsystem in self.get_config_section('os'):
            try:
                self.validator.os(operatingsystem)
            except MultipleInvalid as e:
                log.log(log.LOG_ERROR, "Cannot create Operating System '{0}': \n YAML validation Error: {1}".format(operatingsystem, e))
                sys.exit(1)
            try:
                os_id = self.fm.operatingsystems.show(operatingsystem['description'])['id']
                log.log(log.LOG_DEBUG, "Operating System '{0}' (id={1}) already present.".format(operatingsystem, os_id))
            except:
                log.log(log.LOG_INFO, "Create Operating System '{0}'".format(operatingsystem))
                os_tpl = {
                    'name':             operatingsystem['name'],
                    'description':      operatingsystem['description'],
                    'major':            operatingsystem['major'],
                    'minor':            operatingsystem['minor'],
                    'family':           operatingsystem['family'],
                    'release_name':     operatingsystem['release-name'],
                    'password_hash':    operatingsystem['password-hash']
                }
                os_obj = self.fm.operatingsystems.create(operatingsystem=os_tpl)

                #  host_params
                if operatingsystem['parameters'] is not None:
                    for name,value in operatingsystem['parameters'].iteritems():
                        p = {
                            'name':     name,
                            'value':    value
                        }
                        try:
                            self.fm.operatingsystems.parameters_create(os_obj['id'], p )
                        except:
                            log.log(log.LOG_WARN, "Error adding host parameter '{0}'".format(name))


    def load_config_os_link(self):
        log.log(log.LOG_INFO, " Connecting os System Items (Provisioning Templates, Media, Partition Tables)")
        for operatingsystem in self.get_config_section('os'):
            try:
                self.validator.os(operatingsystem)
            except MultipleInvalid as e:
                log.log(log.LOG_ERROR, "Cannot update Operating System '{0}': \n YAML validation Error: {1}".format(operatingsystem, e))
                sys.exit(1)

            os_obj = False
            try:
                os_obj = self.fm.operatingsystems.show(operatingsystem['description'])
            except:
                log.log(log.LOG_WARN, "Cannot get ID of Operating System '{0}', skipping".format(operatingsystem))
            if os_obj:

                # link Partition Tables
                add_pt = []
                for os_ptable in operatingsystem['partition-table']:
                    try:
                        ptable_id = self.fm.ptables.show(os_ptable['name'])['id']
                        add_pt.append({'id': ptable_id})
                    except:
                        log.log(log.LOG_WARN, "Cannot get ID of Partition Table '{0}', skipping".format(os_ptable))

                # link architectures
                add_arch = []
                for os_arch in operatingsystem['architecture']:
                    try:
                        arch_id = self.fm.architectures.show(os_arch['name'])['id']
                        add_arch.append(arch_id)
                    except:
                        log.log(log.LOG_WARN, "Cannot get ID of Architecture '{0}', skipping".format(os_arch))

                # link medium
                add_medium = []
                medialist = self.fm.media.index(per_page=99999)['results']
                for os_media in operatingsystem['medium']:
                    for mediac in medialist:
                        if mediac['name'] == os_media['name']:
                            add_medium.append(mediac['id'])

                # link Provisioning Templates
                add_osdef = []
                add_provt = []
                ptlist = self.fm.provisioning_templates.index(per_page=99999)['results']
                for os_pt in operatingsystem['provisioning-template']:
                    for ptc in ptlist:
                        if ptc['name'] == os_pt['name']:
                            pto = {
                                #'id':                       os_obj['id'],
                                #'config_template_id':       ptc['id'],
                                'template_kind_id':         ptc['template_kind_id'],
                                'provisioning_template_id': ptc['id'],
                            }
                            add_osdef.append(pto)
                            add_provt.append(ptc['id'])

                # now all mapping is done, update os
                update_tpl = {}
                update_osdef = {}
                if add_pt: update_tpl['ptables'] = add_pt
                if add_arch: update_tpl['architecture_ids']         = add_arch
                if add_medium: update_tpl['medium_ids']             = add_medium
                if add_provt:
                    update_tpl['provisioning_template_ids']           = add_provt
                    update_osdef['os_default_templates_attributes']   = add_osdef

                log.log(log.LOG_INFO, "Linking Operating System '{0}' to Provisioning Templates, Media and Partition Tables".format(operatingsystem))

                try:
                    self.fm.operatingsystems.update(os_obj['id'], update_tpl)
                    if add_provt:
                        self.fm.operatingsystems.update(os_obj['id'], update_osdef)
                except:
                    log.log(log.LOG_DEBUG, "An Error Occured when linking Operating System '{0}' (non-fatal)".format(operatingsystem))



    def load_config_hostgroup(self):
        log.log(log.LOG_INFO, "Load hostgroups)")
        hg_parent = hg_os = hg_arch = hg_medium = hg_parttbl = False
        for hostgroup in self.get_config_section('hostgroup_default'):

            #validate yaml
            try:
                self.validator.hostgroup_default(hostgroup)
            except MultipleInvalid as e:
                log.log(log.LOG_ERROR, "Cannot create hostgroup_default '{0}': \n YAML validation Error: {1}".format(hostgroup, e))
                sys.exit(1)
            #find parent hostgroup_default
            try:
                hg_parent = self.fm.hostgroups.show(hostgroup['parent'])['id']
            except:
                log.log(log.LOG_DEBUG, "Cannot get ID of Parent Hostgroup '{0}', skipping".format(hostgroup['parent']))

            # find operatingsystem
            try:
                hg_os = self.fm.operatingsystems.show(hostgroup['os'])['id']
            except:
                log.log(log.LOG_DEBUG, "Cannot get ID of Operating System '{0}', skipping".format(hostgroup['os']))

            # find architecture
            try:
                hg_arch = self.fm.architectures.show(hostgroup['architecture'])['id']
            except:
                log.log(log.LOG_DEBUG, "Cannot get ID of Architecture '{0}', skipping".format(hostgroup['architecture']))

            # find medium
            medialist = self.fm.media.index(per_page=99999)['results']
            for mediac in medialist:
                if (mediac['name'] == hostgroup['medium']):
                    hg_medium = mediac['id']
            if not hg_medium:
                log.log(log.LOG_DEBUG, "Cannot get ID of Medium '{0}', skipping".format(hostgroup['medium']))

            # find partition table
            try:
                hg_parttbl = self.fm.ptables.show(hostgroup['partition-table'])['id']
            except:
                log.log(log.LOG_DEBUG, "Cannot get ID of Partition Table '{0}', skipping".format(hostgroup['partition-table']))


        for hostgroup in self.get_config_section('hostgroup'):

            #validate yaml
            try:
                self.validator.hostgroup(hostgroup)
            except MultipleInvalid as e:
                log.log(log.LOG_ERROR, "Cannot create Hostgroup '{0}': \n YAML validation Error: {1}".format(hostgroup, e))
                sys.exit(1)

            # check if hostgroup already exists
            try:
                hg_id = self.fm.hostgroups.show(hostgroup['name'])['id']
                log.log(log.LOG_ERROR, "Hostgroup '{0}' (id={1}) already present.".format(hostgroup, hg_id))
                sys.exit(1)
            # hg is not existent on fm, creating
            except:
                log.log(log.LOG_INFO, "Create Hostgroup '{0}'".format(hostgroup))
                hg_domain = hg_subnet = False

                # find domain
                try:
                    hg_domain = self.fm.domains.show(hostgroup['domain'])['id']
                except:
                    log.log(log.LOG_DEBUG, "Cannot get ID of Domain '{0}', skipping".format(hostgroup['domain']))

                # find subnet
                try:
                    hg_subnet = self.fm.subnets.show(hostgroup['subnet'])['id']
                except:
                    log.log(log.LOG_DEBUG, "Cannot get ID of Subnet '{0}', skipping".format(hostgroup['subnet']))

                # build array
                hg_arr = {
                    'name':         hostgroup['name']
                }
                if hg_parent:
                    hg_arr['parent_id']           = hg_parent
                if hg_os:
                    hg_arr['operatingsystem_id']  = hg_os
                if hg_arch:
                    hg_arr['architecture_id']     = hg_arch
                if hg_medium:
                    hg_arr['medium_id']           = hg_medium
                if hg_domain:
                    hg_arr['domain_id']           = hg_domain
                if hg_parttbl:
                    hg_arr['ptable_id']           = hg_parttbl
                if hg_subnet:
                    hg_arr['subnet_id']           = hg_subnet
                hg_arr['root_pass']               = hostgroup['root-pass']

                # send to foreman-api
                try:
                    hg_api_answer = self.fm.hostgroups.create(hostgroup=hg_arr)
                except ForemanException as e:
                    msg = self.get_api_error_msg(e)
                    log.log(log.LOG_ERROR, "An Error Occured when creating Hostgroup '{0}', api says: '{1}'".format(hostgroup['name'], msg) )
                    sys.exit(1)


    def load_config_host(self):
        log.log(log.LOG_INFO, "Load hosts")
        for hostc in self.get_config_section('hosts'):

            try:
                self.validator.host(hostc)
            except MultipleInvalid as e :
                log.log(log.LOG_ERROR, "Cannot create hosts '{0}': \n YAML validation Error: {1}".format(hostc, e))
                sys.exit(1)

            domain = None
            try:
                hostgroupname = hostc['hostgroup']
                domain = self.fm.hostgroups.show(hostgroupname)['domain_name']
            except:
                log.log(log.LOG_ERROR, "Cannot get domain in hostgroup  '{0}'".format(hostgroupname))


            hostname = "{0}.{1}".format(hostc['name'], domain)
            try:
                host_id = self.fm.hosts.show(hostname)['id']
                log.log(log.LOG_DEBUG, "Host '{0}' (id={1}) already present.".format(hostname, host_id))
                continue
            except:
                log.log(log.LOG_INFO, "Create Host '{0}'".format(hostname))

            # temporaty, change it on the future
            device = self.get_config_section('device_identifier')[0]['name']
            host_tpl = {
                'build':                'true',
                'name':                 hostc['name'],
                'mac':                  hostc['mac'],
                'ip':                   hostc['ip'],
                'interfaces_attributes': [{'identifier': device}],
            }
            hostgroup_id = False
            try:
                hostgroup_id = self.fm.hostgroups.show(hostgroupname)['id']
                if hostgroup_id:
                    log.log(log.LOG_DEBUG, "Add Hostgroup %s to the host" % hostgroup_id)
                    host_tpl['hostgroup_id'] = hostgroup_id
            except:
                    log.log(log.LOG_ERROR, "Hostgroup {0} does not exist".format(hostc['hostgroup']))

            try:
                self.fm.hosts.create( host = host_tpl )
                log.log(log.LOG_INFO, "Create new host '{0}'".format(hostname))
            except ForemanException as e:
                msg = self.get_api_error_msg(e)
                log.log(log.LOG_ERROR, "Error creating new host '{0}' \n error: '{1}'".format(host_tpl,msg))
