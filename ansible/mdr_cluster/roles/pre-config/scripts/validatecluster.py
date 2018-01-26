import os
import sys

import yaml

import log
from config_schema import Validator
from error import MatchInvalid,Invalid
from error import MultipleInvalid



validator = Validator()
globalConfigData = ''
commonHostGroups = {}
commonHostGroupMap = {}
commonHostGroupIpMap = {}



def checkHostGroupNameExists(groupName):

	if groupName not in commonHostGroups:
		raise Invalid('Hostgroup \'{0}\' doesn\'t exist\'s in {1}'.format(groupName,commonHostGroups))

	if len(commonHostGroupMap[groupName]) == 0:
		raise Invalid('No hosts mapped to hostgroup \'{0}\' in {1}'.format(groupName,commonHostGroups))



def loadcommonHostgroupInfo(configdata):

	try:

            validator.config(configdata)
        except MultipleInvalid as e:
             for error in e.errors:
                log.log(log.LOG_ERROR, "YAML validation Error: message:{0} in {1}".format(error, configdata))
             sys.exit(1)

	data = configdata.get('common',{})
	try:
	   validator.common(data)
	except MultipleInvalid as e:
		for error in e.errors:
			log.log(log.LOG_ERROR, "YAML validation Error: message:{0} in {1}".format(error, data.get('common')))
		sys.exit(1)

	hostgroups = data.get('hostgroups')

	for hostgroup in hostgroups:
			try:
			  validator.common_hostgroup(hostgroup)
			  if hostgroup['name'] not in commonHostGroups:
				commonHostGroups[hostgroup['name']] = hostgroup
				commonHostGroupMap[hostgroup['name']] = {}
			  else:
				  raise Invalid('duplicate hostgroup name:'+hostgroup['name'])
			except MultipleInvalid as e:
				for error in e.errors:
					log.log(log.LOG_ERROR, "YAML validation Error: message:{0} in {1}".format(error, hostgroup))
				sys.exit(1)
			except Invalid as e:
				log.log(log.LOG_ERROR, "YAML validation Error: message:{0} in {1}".format(e, hostgroup))
				sys.exit(1)

	for primary_host in data.get('primary_hosts'):
		try:
			#IP Consistancy if dns_enabled = No
			if globalConfigData["default"].get('dns_enabled') == False:
				validator.common_primary_host_default(primary_host)
				if primary_host['hostgroup'] not in commonHostGroups:
					raise Invalid('Unknown hostgroup {0} mapped to host {1}'.format(primary_host['hostgroup'],primary_host['name']))
				else:
					if primary_host['ip'] in commonHostGroupIpMap:
						raise Invalid('ip \'{0}\' mapped to two host groups {1} & {2}'.format(primary_host['ip'],commonHostGroupIpMap.get(primary_host['ip']),primary_host['hostgroup']))
					else:
						commonHostGroupIpMap[primary_host['ip']] = primary_host['hostgroup']
					fqdn = primary_host['name']+'.'+commonHostGroups[primary_host['hostgroup']].get('domain')
					primary_host['fqdn'] = fqdn
					commonHostGroupMap[primary_host['hostgroup']][fqdn] = primary_host
					commonHostGroupIpMap[primary_host.get('ip')] = primary_host['hostgroup']

		        #Ignore IP if dns_enabled = Yes
			else:
				validator.common_primary_host(primary_host)
				if primary_host['hostgroup'] not in commonHostGroups:
					raise Invalid('Unknown hostgroup {0} mapped to host {1}'.format(primary_host['hostgroup'],primary_host['name']))
				else:
					primary_host['fqdn'] = primary_host['name'] + '.' + commonHostGroups[primary_host['hostgroup']].get(
						'domain')
				fqdn = primary_host['name'] + '.' + commonHostGroups[primary_host['hostgroup']].get('domain')
				primary_host['fqdn'] = fqdn
				commonHostGroupMap[primary_host['hostgroup']][fqdn] = primary_host


		except Invalid as e:
			log.log(log.LOG_ERROR, "YAML validation Error: common[primary_hosts]:{0} in {1}".format(e, primary_host))
			sys.exit(1)


def validateConfigFile(configdata):


    try:
       validator.config( configdata)
    except MultipleInvalid as e:
	for error in e.errors:
		log.log(log.LOG_ERROR, "YAML validation Error: message:{0} in {1}".format(error, configdata))
	sys.exit(1)

    try:
           for configService in configdata:
        	serviceData = configdata.get(configService)
		msg = 'Success'
		msglevel = log.LOG_INFO_RM
		if configService == 'default':
			validator.default(serviceData)
                elif configService == 'httpd':
                        validator.httpd(serviceData)

		elif configService == 'ambari':
			checkHostGroupNameExists(serviceData.get('hostgroup'))
         		validator.hdpambari(configdata)
		elif configService == 'hdp':
			validator.hdp(serviceData)
			component_groups = serviceData.get('component_groups')
			for component_group in component_groups :
				try:
					validator.component_group(component_groups.get(component_group))
				except Invalid as exe:
				   log.log(log.LOG_ERROR, configService + ": component_groups[" + component_group + "] : YAML validation Error: {0} in  {1}".format(exe.error_message, component_groups.get(component_group)))
				   sys.exit(1)
				host_groups = serviceData.get('hostgroups')
				for host_group  in host_groups:
					host_group_name = host_group.keys()[0]
				try:
					validator.host_group(host_group[host_group_name])
					checkHostGroupNameExists(host_group[host_group_name]['hostgroup'])
				except Invalid as exe:
					log.log(log.LOG_ERROR,
							configService + ": hostgroups[" + host_group_name +"][hostgroup] : YAML validation Error: {0} in  {1}".format(
								exe.error_message, host_group))
					sys.exit(1)

                elif configService == 'hdp_test':
                    validator.hdp_test(serviceData)
                    checkHostGroupNameExists(serviceData.get('hostgroup'))

                elif configService == 'kibana':
                    validator.kibana(serviceData)
                    checkHostGroupNameExists(serviceData.get('hostgroup'))

                elif configService == 'postgres':
                    validator.postgres(serviceData)
                    checkHostGroupNameExists(serviceData.get('hostgroup'))

                elif configService == 'activemq':
                    validator.activemq(serviceData)
                    checkHostGroupNameExists(serviceData.get('hostgroup'))

                elif configService == 'es_master':
                    validator.es_master(serviceData)
                    checkHostGroupNameExists(serviceData.get('hostgroup'))
                    validator.es_config(serviceData['es_config'])

                elif configService == 'es_node':
                    validator.es_node(serviceData)
                    checkHostGroupNameExists(serviceData.get('hostgroup'))
                    validator.es_config(serviceData['es_config'])


                elif configService == 'apache':
                    validator.apache(serviceData)
                    checkHostGroupNameExists(serviceData.get('hostgroup'))

                elif configService == 'mongodb':
                    validator.mongodb(serviceData)
                    checkHostGroupNameExists(serviceData.get('hostgroup'))

                elif configService == 'docker':
                    validator.docker(serviceData)
                    checkHostGroupNameExists(serviceData.get('hostgroup'))
                elif configService == 'common':
                    continue
                else:
                    msg = 'Skipping'
                    msglevel = log.LOG_WARN_RM

                log.log(log.LOG_INFO, 'Yaml validation : {0}  {1}!'.format(configService, log.log(msglevel, msg)))

    except MultipleInvalid as e:
        for error in e.errors:
           log.log(log.LOG_ERROR, configService + " : YAML validation Error:{0} in {1}".format(error, configdata[configService]))
        sys.exit(1)
    except MatchInvalid as e:
        log.log(log.LOG_ERROR,
				configService + " : YAML validation Error:{0} in {1}".format(e.error_message, configdata[configService]))
        sys.exit(1)
    except Invalid as e:
        log.log(log.LOG_ERROR,
				configService + " : YAML validation Error:{0} in {1}".format(e.error_message,configdata[configService]))
        sys.exit(1)


def updateConfigData(configData):
     global globalConfigData
     global commonHostGroupIpMap
     global commonHostGroups
     global commonHostGroupMap
     globalConfigData = configData
     commonHostGroups = {}
     commonHostGroupMap = {}
     commonHostGroupIpMap = {}

def main(configdata):
    try:
        updateConfigData(configdata)
        loadcommonHostgroupInfo(configdata)
        validateConfigFile(configdata)

    except yaml.YAMLError as exc:
        log.log(log.LOG_ERROR, exc)
        sys.exit(1)
