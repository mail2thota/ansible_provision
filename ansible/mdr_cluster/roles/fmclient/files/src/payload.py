#!/usr/bin/python
# -*- coding: utf8 -*-
#Copyright:@BaeSystemsAI
#Original author: Heri Sutrisno
#Email:harry.sutrisno@baesystems.com
#Description:payload foreman resources

import sys
import log
import config_templates
from foreman_base import ForemanBase
from pprint import pprint
from foreman.client import Foreman, ForemanException

class ForemanLoad(ForemanBase):
    
    def load_config_template(self):
        log.log(log.LOG_INFO, "Update Global Templates")
        full_path = self.get_repo_ip()
        config_templates.init(full_path)
        try:
            kick_id = self.fm.config_templates.show('Kickstart default')['id']
            pxelinux_id = self.fm.config_templates.show('Kickstart default PXELinux')['id']
            log.log(log.LOG_DEBUG, "get Kickstarter default id:'{0}'".format(kick_id))
            log.log(log.LOG_DEBUG, "get Kickstarter PXELinux id:'{0}'".format(pxelinux_id))

        except:
            log.log(log.LOG_ERROR, "Kickstarter default id:'{0}' is not exist".format(kick_id))
            log.log(log.LOG_ERROR, "Kickstarter default PXELinux id:'{0}' is not exist".format(pxelinux_id))
            sys.exit(1)
        self.fm.config_templates.update({'locked': False},kick_id)       
        self.fm.config_templates.update({'template': config_templates.kickstarter_default['template']},kick_id)
        self.fm.config_templates.update({'locked': True},kick_id)

        self.fm.config_templates.update({'locked': False},pxelinux_id)
        self.fm.config_templates.update({'template': config_templates.kickstarter_pxelinux['template']},pxelinux_id)
        self.fm.config_templates.update({'locked': True},pxelinux_id)

        try:
            build_template = self.fm.config_templates.build_pxe_default()
            log.log(log.LOG_INFO, "Template:'{0}'".format(build_template))
        except:
            log.log(log.LOG_ERROR, "template can not be built")
            sys.exit(1)

    def load_global_params(self):
        log.log(log.LOG_INFO, "Load Global Parameters")
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
                arch_id = self.fm.architectures.show(arch['name'])['id']
                log.log(log.LOG_DEBUG, "Architecture '{0}' (id={1}) already present.".format(arch, arch_id))
            except:
                log.log(log.LOG_INFO, "Create Architecture '{0}'".format(arch))
                self.fm.architectures.create( architecture = { 'name': arch['name'] } )

    def load_config_domain(self):
        log.log(log.LOG_INFO, "Load Domains")
        for domain in self.get_config_section('domain'):
            try:
                dom_id = self.fm.domains.show(domain['name'])['id']
                log.log(log.LOG_DEBUG, "Domain '{0}' (id={1}) already present.".format(domain, dom_id))
            except:
                log.log(log.LOG_INFO, "Create Domain '{0}'".format(domain['name']))
                self.fm.domains.create(domain = {'name': domain['name'], 'fullname': domain['fullname']})

    def load_config_medium(self):
        self.get_repo_ip
        log.log(log.LOG_INFO, "Load Media")
        medialist = self.fm.media.index(per_page=99999)['results']
        for medium in self.get_config_section('medium'):
            full_path = self.get_repo_ip() + medium['path']
            try:
                medium_id = self.fm.media.show(medium['name'])['id']
                log.log(log.LOG_DEBUG, "Medium '{0}' (id={1}) already present.".format(medium, medium_id))
            except:
                medium_tpl = {
                    'name':        medium['name'],
                    'path':        full_path,
                    'os_family':   medium['os_family']
                    }
                self.fm.media.create(medium=medium_tpl)


    def load_ptable(self):
        log.log(log.LOG_INFO, "Load Partition Tables")
        ptable_sys=self.get_config_section('partition_system')
        for ptable in self.get_config_section('partition_table'):
            
            ptable_snippet=config_templates.ptable_init(ptable,ptable_sys)
            try:
                ptable_id = self.fm.ptables.show(ptable['name'])['id']
                log.log(log.LOG_INFO, "Partition Table '{0}' (id={1}) already present.".format(ptable['name'], ptable_id))
            except:
                log.log(log.LOG_INFO, "Create Partition Table '{0}'".format(ptable['name']))
                ptable_tpl = {
                    'name':             ptable['name'],
                    'layout':           ptable_snippet['snippet'],
                    'snippet':          0,
                    'audit_comment':    'initial import',
                    'locked':           0,
                    'os_family':        'Redhat'
                }
                self.fm.ptables.create( ptable = ptable_tpl )


    def load_config_settings(self):
        log.log(log.LOG_INFO, "Load Foreman Settings")
        for setting in self.get_config_section('setting'):
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
        log.log(log.LOG_INFO, "Load Unattended And Foreman URL Settings")
        try:
            settingunatt_id = self.fm.settings.show('unattended_url')['id']
            settingurl_id = self.fm.settings.show('foreman_url')['id']
        except MultipleInvalid as e:
            log.log(log.LOG_ERROR, "Cannot get ID of Setting '{0}' error: '{1}', exit".format('unattended_url and foreman_url', e))
            sys.exit(1)
        fm_ip = self.get_fm_ip()
        settingurl_tpl = {
            'value':         fm_ip,
        }
        log.log(log.LOG_INFO, "Update Setting Unattended_url '{0}'".format('unattended_url and foreman_url'))
        self.fm.settings.update(settingurl_tpl, settingunatt_id)
        self.fm.settings.update(settingurl_tpl, settingurl_id)


    def load_config_smartproxy(self):
        log.log(log.LOG_INFO, "Load Smart Proxies")
        fmproxy = self.get_config_section('foreman_proxy')
        fmproxy_port = fmproxy['port']
        fm_ip = self.get_fm_ip() 
        foreman_proxyip = fm_ip + ":" + str(fmproxy_port)
        try:
            proxy_id = self.fm.smart_proxies.show(self.get_fm_hostname())['id']
            log.log(log.LOG_DEBUG, "Proxy '{0}' (id={1}) is already present.".format(self.get_fm_hostname(), proxy_id))
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
                sys.exit(1)


    def load_config_subnet(self):
        log.log(log.LOG_INFO, "Load Subnets")
        subnet_tpl_dft = {
              'dhcp-proxy': self.get_fm_hostname(),
              'tftp-proxy': self.get_fm_hostname(),
              'boot-mode' : 'Static',
              'network-type': 'IPv4',
#              'dns-proxy': self.get_fm_hostname(),
              'ipam': 'None',
        }
        for subnet in self.get_config_section('subnet'):
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
                    'dns_primary':      subnet['dns_primary'],
                    'dns_secondary':    subnet['dns_secondary'],
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
                os_id = self.fm.operatingsystems.show(operatingsystem['name'])['id']
                log.log(log.LOG_DEBUG, "Operating System '{0}' (id={1}) already present.".format(operatingsystem, os_id))
            except:
                log.log(log.LOG_INFO, "Create Operating System '{0}'".format(operatingsystem))
                os_tpl = {
                    'name':             operatingsystem['name'],
                    'description':      operatingsystem['name'],
                    'major':            7,
                    'minor':            7,
                    'family':           operatingsystem['family'],
                    'password_hash':    operatingsystem['password_hash']
                }
                os_obj = self.fm.operatingsystems.create(operatingsystem=os_tpl)


    def load_config_os_link(self):
        log.log(log.LOG_INFO, " Connecting OS System Items With (Provisioning Templates, Media, Partition Tables)")
        for operatingsystem in self.get_config_section('os'):
            os_obj = False
            try:
                os_obj = self.fm.operatingsystems.show(operatingsystem['name'])
            except:
                log.log(log.LOG_ERROR, "Cannot get ID of Operating System '{0}', skipping".format(operatingsystem))
                sys.exit(1)

            if os_obj:
                # link Partition Tables
                add_pt = []
                for os_ptable in self.get_config_section('partition_table'):
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
                for os_pt in operatingsystem['provisioning_template']:
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
        log.log(log.LOG_INFO, "Load Hostgroups)")
        hg_os = hg_arch = hg_medium = hg_parttbl = False
        hostgroup = self.get_config_section('hostgroup_system')
        # find operatingsystem
        try:
            hg_os = self.fm.operatingsystems.show(hostgroup['os'])['id']
        except:
            log.log(log.LOG_ERROR, "Cannot get ID of Operating System '{0}'".format(hostgroup['os']))
            sys.exit(1)
        # find architecture
        try:
            hg_arch = self.fm.architectures.show(hostgroup['architecture'])['id']
        except:
            log.log(log.LOG_ERROR, "Cannot get ID of Architecture '{0}'".format(hostgroup['architecture']))
            sys.exit(1)
        # find medium
        medialist = self.fm.media.index(per_page=99999)['results']
        for mediac in medialist:
            if (mediac['name'] == hostgroup['medium']):
                hg_medium = mediac['id']
        if not hg_medium:
            log.log(log.LOG_ERROR, "Cannot get ID of Medium '{0}'".format(hostgroup['medium']))
            sys.exit(1)

        for hostgroup in self.get_common_section('hostgroups'):

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
                    log.log(log.LOG_ERROR, "Cannot get ID of Domain '{0}'".format(hostgroup['domain']))
                    sys.exit(1)   
                # find subnet
                try:
                    hg_subnet = self.fm.subnets.show(hostgroup['subnet'])['id']
                except:
                    log.log(log.LOG_ERROR, "Cannot get ID of Subnet '{0}'".format(hostgroup['subnet']))
                    sys.exit(1)

                 # find partition table***
                try:
                    hg_parttbl = self.fm.ptables.show(hostgroup['partition_table'])['id']
                except:
                    log.log(log.LOG_ERROR, "Cannot get ID of Partition Table '{0}'".format(hostgroup['partition_table']))
                    sys.exit(1)

                # build array
                hg_arr = {
                    'name':         hostgroup['name']
                }
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
                hg_arr['root_pass']               = self.get_node_pass()

                # send to foreman-api
                try:
                    hg_api_answer = self.fm.hostgroups.create(hostgroup=hg_arr)
                except ForemanException as e:
                    msg = self.get_api_error_msg(e)
                    log.log(log.LOG_ERROR, "An Error Occured when creating Hostgroup '{0}', api says: '{1}'".format(hostgroup['name'], msg) )
                    sys.exit(1)

    def search_mutual_exclusive(self,section,name):
        log.log(log.LOG_INFO, "Search Mutual Exclusive Of Sections")
        for key,value in section.iteritems():
            if value == name:
                return section, True

        log.log(log.LOG_INFO, "'{0}'is  not subset interface of: '{1}' in YML configuration, skip it".format(section['primary'],name))
        return section,False


    def load_config_host(self):
        log.log(log.LOG_INFO, "Load Hosts")
        for hostc in self.get_common_section('primary_hosts'):
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
                log.log(log.LOG_INFO, "Set new host '{0}'".format(hostname))

            host_tpl = {
                'build':                'true',
                'name':                 hostc['name'],
                'mac':                  hostc['mac'],
                'ip':                   hostc['ip'],
                'interfaces_attributes': [{'identifier': 'eth0','primary': 1}],
            }
            self.ifexist=True
            if self.ifexist: 
                domainid = self.fm.domains.show(domain)['id']
                count_eth=0
                for sechost in self.get_common_section('secondary_hosts'):
            	    sec,sec_status=self.search_mutual_exclusive(sechost,hostc['name'])
                    if sec_status:
                        count_eth +=1
                        eth_var='eth{0}'.format(count_eth)

                        subnet = self.fm.subnets.show(sec['subnet'])['id']
                        secondary_tpl={
                            'mac':                  sec['mac'],
                            'identifier':           eth_var,
                            'primary':              0,            
                            'domain_id':            domainid,
                            'subnet_id':            subnet,
                            'ip':                   sec['ip'],
                        }
                        host_tpl['interfaces_attributes'].append(secondary_tpl)
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










