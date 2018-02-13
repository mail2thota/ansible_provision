import os
import sys

import yaml

import log
from config_schema import Validator
from error import MatchInvalid,Invalid
from error import MultipleInvalid



validator = Validator()
globalConfigData = ''
excludeSections = ['common','foreman']
globalEnvHostGroupMap = {}

def checkHostGroupValidity(clustername,hostgroupName,dns_enabled):

	if hostgroupName not in envHostGroupsMap:
		log.log(log.LOG_ERROR,"{0}: Hostgroup or tag [{1}] doesn\'t exist\'s ".format(clustername,hostgroupName))
		sys.exit(1)
	hostinfo = envHostGroupsMap[hostgroupName]['hosts']

	if len(hostinfo) == 0:
		log.log(log.LOG_ERROR,'{0}: Config validation Error: No hosts mapped to hostgroup {1}'.format(clustername,hostgroupName))
		sys.exi(1)
	if dns_enabled is not True:
		for host in hostinfo:
			#Check for ip if dns  not enabled
			if host['ip'] is None:
				log.log(log.LOG_ERROR,"{0}: Config validation Error: ip adress required for the host [{1}]".format(clustername,host['name']))
				sys.exit(1)






def validatePreRequistives(configdata,clustername):

	#Validate  mandatory top level sections such as httpd & default
	try:
		validator.config(configdata)
	except MultipleInvalid as e:
		for error in e.errors:
			log.log(log.LOG_ERROR,'{0}  Config validation Error message:{1}'.format(clustername,error))
		sys.exit(1)
	#Check default section for dns_enabled flag
	defaultData  = configdata.get('default',{})
	try:
		validator.default(defaultData)

	except MultipleInvalid as e:
		for error in e.errors:
		    log.log(log.LOG_ERROR, "{0} :[default] Config Validation Error:{1} in {2}".format(clustername,error,defaultData))
		sys.exit(1)

	except MatchInvalid as e:
		log.log(log.LOG_ERROR, "{0} : [default] Config Validation Error:{1} in {2}".format(clustername,e,defaultData))
		sys.exit(1)

	except Invalid as e:
		log.log(log.LOG_ERROR, "{0} : [default] Config Validation Error:{1} in {2}".format(clustername,e,defaultData))
		sys.exit(1)

	#Validate httpd data
	httpdData = configdata.get('httpd')
	try:
		validator.httpd(httpdData)
		httpdconfig = httpdData.get('config')
		if httpdconfig == None:
			log.log(log.LOG_INFO, '{0} : assuming httpd without any configuration'.format(clustername))
		else:
			for balancer in httpdconfig:
				try:
					validator.httpd_balancer(httpdconfig[balancer])
				except Invalid as e:
					log.log(log.LOG_ERROR,"{0} config Error: {1} in {2}".format(clustername,e.error_message,httpdconfig[balancer]))
					sys.exit(1)
	except MultipleInvalid as e:
		for error in e.errors:
		    log.log(log.LOG_ERROR, "{0} :[httpd] Config Validation Error:{1} in {2}".format(clustername,error,defaultData))
		sys.exit(1)

	except MatchInvalid as e:
		log.log(log.LOG_ERROR, "{0} : [httpd] Config Validation Error:{1} in {2}".format(clustername,e,defaultData))
		sys.exit(1)

	except Invalid as e:
		log.log(log.LOG_ERROR, "{0} : [httpd] Config Validation Error:{1} in {2}".format(clustername,e,defaultData))
		sys.exit(1)


	#Validate ambari data
	ambariData = configdata.get('ambari')
	if ambariData is not None:
		try:
			validator.ambari(ambariData)

		except MultipleInvalid as e:
			for error in e.errors:
				log.log(log.LOG_ERROR, "{0} :[ambari] Config Validation Error:{1} in {2}".format(clustername,error,ambariData))
			sys.exit(1)

		except MatchInvalid as e:
			log.log(log.LOG_ERROR, "{0} : [ambari] Config Validation Error:{1} in {2}".format(clustername,e,ambariData))
			sys.exit(1)

		except Invalid as e:
			log.log(log.LOG_ERROR, "{0} : [ambari] Config Validation Error:{1} in {2}".format(clustername,e,ambariData))
			sys.exit(1)


	hdpData = configdata.get('hdp')
	if hdpData is not None:
		try:
			#Check for ambari first then validate hdp
			try:
				validator.hdpambari(configdata)
			except Invalid as e:
				log.log(log.LOG_ERROR, "{0} : [hdp] Config Validation  Error:{1} in {2}".format(clustername, e, hdpData))
				sys.exit(1)

			validator.hdp(hdpData)
			component_groups = hdpData.get('component_groups')
			for component_group in component_groups :
				try:
					validator.component_group(component_groups.get(component_group))
				except Invalid as exe:
					log.log(log.LOG_ERROR,"{0}[hdp]: component_groups[{1}] : Config validation Error: {2} in  {3}".format(clustername,component_group,exe.error_message, component_groups.get(component_group)))
					sys.exit(1)

				host_groups = hdpData.get('hostgroups')
				for host_group  in host_groups:
					host_group_name = host_group.keys()[0]
					try:
						validator.host_group(host_group[host_group_name])

					except Invalid as exe:
						log.log(log.LOG_ERROR,"{0}[hdp]: hostgroups[{1}] : Config validation Error: {2} in  {3}".format(clustername,host_group_name,exe.error_message, host_group))
						sys.exit(1)
		except MultipleInvalid as e:
			for error in e.errors:
				log.log(log.LOG_ERROR,
						"{0} :[hdp] Config Validation Error:{1} in {2}".format(clustername, error, hdpData))
			sys.exit(1)

		except MatchInvalid as e:
			log.log(log.LOG_ERROR, "{0} : [hdp] Config Validation Error:{1} in {2}".format(clustername, e, hdpData))
			sys.exit(1)

		except Invalid as e:
			log.log(log.LOG_ERROR, "{0} : [hdp] Config Validation Error:{1} in {2}".format(clustername, e, hdpData))
			sys.exit(1)

	# Validate hdp_test data
	hdptestData = configdata.get('hdp_test')
	if hdptestData is not None:
		try:
			validator.hdp_test(hdptestData)

		except MultipleInvalid as e:
			for error in e.errors:
				log.log(log.LOG_ERROR,
						"{0} :[hdp_test] Config Validation Error:{1} in {2}".format(clustername, error, hdptestData))
			sys.exit(1)

		except MatchInvalid as e:
			log.log(log.LOG_ERROR,
					"{0} : [hdp_test] Config Validation Error:{1} in {2}".format(clustername, e, hdptestData))
			sys.exit(1)

		except Invalid as e:
			log.log(log.LOG_ERROR,
					"{0} : [hdp_test] Config Validation Error:{1} in {2}".format(clustername, e, hdptestData))
			sys.exit(1)

	# Validate kibana data
	kibanaData = configdata.get('kibana')
	if kibanaData is not None:
		try:
			validator.kibana(kibanaData)

		except MultipleInvalid as e:
			for error in e.errors:
				log.log(log.LOG_ERROR,
						"{0} :[kibana] Config Validation Error:{1} in {2}".format(clustername, error, kibanaData))
			sys.exit(1)

		except MatchInvalid as e:
			log.log(log.LOG_ERROR,
					"{0} : [kibana] Config Validation Error:{1} in {2}".format(clustername, e, kibanaData))
			sys.exit(1)

		except Invalid as e:
			log.log(log.LOG_ERROR,
					"{0} : [kibana] Config Validation Error:{1} in {2}".format(clustername, e, kibanaData))
			sys.exit(1)

	# Validate postgres data
	postgresData = configdata.get('postgres')
	if postgresData is not None:
		try:
			validator.postgres(postgresData)

		except MultipleInvalid as e:
			for error in e.errors:
				log.log(log.LOG_ERROR,
						"{0} :[postgres] Config Validation Error:{1} in {2}".format(clustername, error, postgresData))
			sys.exit(1)

		except MatchInvalid as e:
			log.log(log.LOG_ERROR,
					"{0} : [postgres] Config Validation Error:{1} in {2}".format(clustername, e, postgresData))
			sys.exit(1)

		except Invalid as e:
			log.log(log.LOG_ERROR,
					"{0} : [postgres] Config Validation Error:{1} in {2}".format(clustername, e, postgresData))
			sys.exit(1)

	# Validate activemq data
	activemqData = configdata.get('activemq')
	if activemqData is not None:
		try:
			validator.activemq(activemqData)

		except MultipleInvalid as e:
			for error in e.errors:
				log.log(log.LOG_ERROR,
						"{0} :[activemq] Config Validation Error:{1} in {2}".format(clustername, error, activemqData))
			sys.exit(1)

		except MatchInvalid as e:
			log.log(log.LOG_ERROR,
					"{0} : [activemq] Config Validation Error:{1} in {2}".format(clustername, e, activemqData))
			sys.exit(1)

		except Invalid as e:
			log.log(log.LOG_ERROR,
					"{0} : [activemq] Config Validation Error:{1} in {2}".format(clustername, e, activemqData))
			sys.exit(1)


	#Validate es_master data
	es_masterData = configdata.get('es_master')
	if es_masterData is not None:
		try:
			validator.es_master(es_masterData)
			validator.es_config(es_masterData.get('es_config'))

		except MultipleInvalid as e:
			for error in e.errors:
				log.log(log.LOG_ERROR,
						"{0} :[es_master] Config Validation Error:{1} in {2}".format(clustername, error, es_masterData))
			sys.exit(1)

		except MatchInvalid as e:
			log.log(log.LOG_ERROR,
					"{0} : [es_master] Config Validation Error:{1} in {2}".format(clustername, e, es_masterData))
			sys.exit(1)

		except Invalid as e:
			log.log(log.LOG_ERROR,
					"{0} : [es_master] Config Validation Error:{1} in {2}".format(clustername, e, es_masterData))
			sys.exit(1)

	#Validate es_node data
	es_nodeData = configdata.get('es_node')
	if es_nodeData is not None:
		try:
			validator.es_node(es_nodeData)
			validator.es_config(es_nodeData.get('es_config'))
		except MultipleInvalid as e:
			for error in e.errors:
				log.log(log.LOG_ERROR,
						"{0} :[es_node] Config Validation Error:{1} in {2}".format(clustername, error, es_nodeData))
			sys.exit(1)

		except MatchInvalid as e:
			log.log(log.LOG_ERROR,
					"{0} : [es_node] Config Validation Error:{1} in {2}".format(clustername, e, es_nodeData))
			sys.exit(1)

		except Invalid as e:
			log.log(log.LOG_ERROR,
					"{0} : [es_node] Config Validation Error:{1} in {2}".format(clustername, e, es_nodeData))
			sys.exit(1)

	#Validate apache data
	apacheData = configdata.get('apache')
	if apacheData is not None:
		try:
			validator.apache(apacheData)

		except MultipleInvalid as e:
			for error in e.errors:
				log.log(log.LOG_ERROR,
						"{0} :[apache] Config Validation Error:{1} in {2}".format(clustername, error, apacheData))
			sys.exit(1)

		except MatchInvalid as e:
			log.log(log.LOG_ERROR,
					"{0} : [apache] Config Validation Error:{1} in {2}".format(clustername, e, apacheData))
			sys.exit(1)

		except Invalid as e:
			log.log(log.LOG_ERROR,
					"{0} : [apache] Config Validation Error:{1} in {2}".format(clustername, e, apacheData))
			sys.exit(1)

	#Validate mongodb data
	mongodbData = configdata.get('mongodb')
	if mongodbData is not None:
		try:
			validator.mongodb(mongodbData)

		except MultipleInvalid as e:
			for error in e.errors:
				log.log(log.LOG_ERROR,
						"{0} :[mongodb] Config Validation Error:{1} in {2}".format(clustername, error, mongodbData))
			sys.exit(1)

		except MatchInvalid as e:
			log.log(log.LOG_ERROR,
					"{0} : [mongodb] Config Validation Error:{1} in {2}".format(clustername, e, mongodbData))
			sys.exit(1)

		except Invalid as e:
			log.log(log.LOG_ERROR,
					"{0} : [mongodb] Config Validation Error:{1} in {2}".format(clustername, e, mongodbData))
			sys.exit(1)


	#Validate docker data
	dockerData = configdata.get('docker')
	if dockerData is not None:
		try:
			validator.docker(dockerData)

		except MultipleInvalid as e:
			for error in e.errors:
				log.log(log.LOG_ERROR,
						"{0} :[docker] Config Validation Error:{1} in {2}".format(clustername, error, dockerData))
			sys.exit(1)

		except MatchInvalid as e:
			log.log(log.LOG_ERROR,
					"{0} : [docker] Config Validation Error:{1} in {2}".format(clustername, e, dockerData))
			sys.exit(1)

		except Invalid as e:
			log.log(log.LOG_ERROR,
					"{0} : [docker] Config Validation Error:{1} in {2}".format(clustername, e, dockerData))
			sys.exit(1)

def add2GroupsMap(clustername,hostgroupname,envHostMap):

	currentGroups = globalEnvHostGroupMap.get(clustername)
	if hostgroupname not in currentGroups:
		currentGroups.append(hostgroupname)

    #Check for hostgroup tags sharing between two groups
	for envName in globalEnvHostGroupMap:
	  if envName == clustername:
		  continue
	  else:
		  if hostgroupname in globalEnvHostGroupMap[envName]:
			 log.log(log.LOG_ERROR,"Config Error: Cannot share hostgroup [{0}] between environments {1} and {2}".format(hostgroupname,envName,clustername))
			 sys.exit(1)
	#Added to Current Env hostgroup with full details
	if hostgroupname in envHostGroupsMap:
		return
	else:
		hostgroupInfo = envHostMap.get('hostgroups').get(hostgroupname)
		if hostgroupInfo is None:
			hostgroupInfo = envHostMap.get('tags').get(hostgroupname)
		if hostgroupInfo is not None:
			envHostGroupsMap[hostgroupname] = hostgroupInfo



def loadEnvSpecificHostgroups(configdata,clustername,envHostMap):
	isDnsEnabled = configdata.get('default').get('dns_enabled',False)
	globalEnvHostGroupMap[clustername] = []
	for section in configdata:
		if section in excludeSections or section in ['default']:
			continue
		sectionData = configdata[section]
		hostgroupName = None
		if section != 'hdp':
			hostgroupName = sectionData.get('hostgroup')
			add2GroupsMap(clustername,hostgroupName,envHostMap)
		else:
			hdphostgroups = sectionData.get('hostgroups',{})
			for hdphostgroup in hdphostgroups:
				for hdphostgroupInfo in hdphostgroup.values():
					hostgroupName = hdphostgroupInfo.get('hostgroup')
					add2GroupsMap(clustername, hostgroupName, envHostMap)
	#print globalEnvHostGroupMap
	#print envHostGroupsMap





def validateDynamicData(configdata,clustername):

	#Validate Hostgroup Existss or empty
    dns_enabled = configdata.get('default').get('dns_enabled',False)
    for section in configdata:
		sectionData = configdata[section]
		if section not in excludeSections and section not in ['default']:
			if section == 'hdp':
				hdphostgroups = sectionData.get('hostgroups', {})
				for hdphostgroup in hdphostgroups:
					for hdphostgroupInfo in hdphostgroup.values():
						hostgroupName = hdphostgroupInfo.get('hostgroup')
						checkHostGroupValidity(clustername,hostgroupName,dns_enabled)
			else:
				hostgroupName = sectionData.get('hostgroup')
				checkHostGroupValidity(clustername, hostgroupName, dns_enabled)

def updateConfigData(configData):
	 global envHostGroupsMap
	 global globalEnvHostGroupMap
	 envHostGroupsMap = {}


def main(configdata,clustername,envHostMap):
    try:
		updateConfigData(configdata)
		validatePreRequistives(configdata, clustername)
		loadEnvSpecificHostgroups(configdata,clustername,envHostMap)
		validateDynamicData(configdata,clustername)
    except yaml.YAMLError as exc:
        log.log(log.LOG_ERROR, exc)
        sys.exit(1)
