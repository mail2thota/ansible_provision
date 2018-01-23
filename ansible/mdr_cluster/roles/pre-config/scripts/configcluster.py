import os
import sys

import yaml

from scripts import log
from scripts.config_schema import Validator
from scripts.error import MatchInvalid,Invalid
from scripts.error import MultipleInvalid


validator = Validator()
excludeSections = ['foreman','common']

globalHostGroupsMaps = {}

def gethosts(groupName):

    hostgroup = commonHostGroupMap[groupName]
    hosts = []
    for ip in hostgroup:
        hosts.append(hostgroup[ip]['fqdn'])
    return hosts

def gethostNameIpMap(groupName):
    hostgroup = commonHostGroupMap[groupName]
    data = []
    for ip in hostgroup:
        data.append({'ip':ip,'name': hostgroup[ip]['fqdn']})
    return data

def gethostGroupName(serviceName):

    return globalConfigData[serviceName]['hostgroup']

def addToEtcHostsList(groupName):
    hosts = gethostNameIpMap(groupName)
    for host in hosts:
        oshostConfig[host['ip']] = host['name']


def getInventoryHostgroupMap():
	inventoryMap = globalHostGroupsMaps.get(inventoryName)
	if inventoryMap == None:
		globalHostGroupsMaps[inventoryName] = []
		inventoryMap = globalHostGroupsMaps.get(inventoryName)
	return inventoryMap

def generateHdpHostConfig(hdpHostConfig):

    outfile = open(ansiblehostsfile, 'w')
    outfile.write("[hdp]")

    if hdpHostConfig["cluster_type"] == 'single_node':
	hostgroup = globalConfigData["ambari"]['hostgroup']
	for host in gethosts(hostgroup):
		outfile.write("\n" + '{0}'.format(host))
    else:
	for host_group in hdpHostConfig["hostgroups"]:
		host_group_name = host_group.keys()[0]
		host_group_name =  host_group[host_group_name]['hostgroup']
		getInventoryHostgroupMap().append(host_group_name)
		for host in gethosts(host_group_name):
			outfile.write("\n" + '{0}'.format(host))
		addToEtcHostsList(host_group_name)

    log.log(log.LOG_INFO, "Create ansible hdp host group configuration file : hosts")

def generateBluePrint(hdpConfig):

	filePath = "{0}{1}{2}.yml".format(rolesConfigFilesdir,os.sep,hdpConfig["cluster_type"])
	outfile = open(filePath, 'w+')

	blueprint_configuration = hdpConfig.get("blueprint_configuration")

	if blueprint_configuration is None:
		blueprint_configuration = []

	blueprint = {"cluster_name": hdpConfig["cluster_name"], "blueprint_name": hdpConfig["blueprint"],
				 "configurations": blueprint_configuration}

	blueprint["blueprint"] = {"stack_name": "HDP", "stack_version": hdpConfig["stack"], "groups": []}

	if hdpConfig['cluster_type'] == 'multi_node':
		for groupsInfo in hdpConfig["hostgroups"]:
			components = []
			for groupName in groupsInfo:
				groupInfo = groupsInfo[groupName]
				componentset = groupInfo["components"]
				for componentName in componentset:
					if componentName  not in hdpConfig['component_groups']:
						log.log(log.LOG_ERROR, 'hdp: Tried to use the non existance component group [' + componentName + "] in hdp[host_groups][" + groupName + "] Please check and re-run")
						sys.exit(1)
					for component in hdpConfig["component_groups"][componentName]:
						components.append(component)
			hostgroup = groupInfo["hostgroup"]
			components = list(set(components))
			blueprint["blueprint"]["groups"].append(
				{"name": groupName, "cardinality": groupInfo.get("cardinality",1), "hosts": gethosts(hostgroup),
				 "components": components, "configuration": groupInfo.get("configuration",[])})

	elif hdpConfig['cluster_type'] == 'single_node':
		components = []
		for component in hdpConfig["component_groups"]:
			componentInfo = hdpConfig["component_groups"][component]
			for componentName in componentInfo:
				components.append(componentName)
		components = list(set(components))
		blueprint["blueprint"]["groups"].append(
			{"name": "master-1", "cardinality": 1, "hosts": gethosts(gethostGroupName('ambari')), "components": components, "configuration": []})

	yaml.dump(blueprint, outfile, default_flow_style=False, allow_unicode=True)
	log.log(log.LOG_INFO, "blueprint: " + str(blueprint))
	return blueprint


def generateCommonDefaultAllConfigFile(config):
    filePath = "{0}/defaults/default-all".format(path)

    with open(filePath, 'r') as stream:
		try:
			configdata = yaml.load(stream)
			with open(allConfigFile, 'w') as allFile:
				allFile.write("#Generated from default-all file \n")
				for property in configdata:
					allFile.write("\n" + property + ": " + str(configdata[property]))
		except yaml.YAMLError as exc:
			log.log(log.LOG_ERROR, "Unalbe to write the all file" + exc)
			sys.exit(1)


def generateEtcHostFile(config,services):
	osHostsFile = open(etchostsFile, 'w')
	for host in oshostConfig:
		osHostsFile.write(host + " " + oshostConfig[host] + "\n")
	log.log(log.LOG_INFO, 'Generated ip & hostname map file to replace  /etc/hosts in all nodes : host_list')

def generateAnsibleHostFile(config,services):

	 with open(ansiblehostsfile, 'a') as hostFile:
		for service in config:
			if service == "hdp":
				continue
			# Creating/Updating ansible hosts group file
			if "hostgroup" in config[service]:
				if service in services or 'all' in services:
					hostFile.write("\n\n\n[" + service + "]")
					hostgroup = config[service]['hostgroup']
					for host in gethosts(hostgroup):
						hostFile.write("\n" + '{0}'.format(host))

					addToEtcHostsList(hostgroup)
	 log.log(log.LOG_INFO, 'updated ansible hosts file for non hdp components: hosts')

def generateAnsibleAllFile(config,services):
	fileMode = None
	# Adding the properties to all file

	isAllConfigFileExists = os.path.exists(allConfigFile)
	inventoryMap = getInventoryHostgroupMap()


	if isAllConfigFileExists:
		fileMode = 'a'
	else:
		fileMode = 'w'
	with open(allConfigFile, fileMode) as allFile:
		allFile.write("\n\n\n\n#Generated from config.yaml ")
		for service in config:
			if service not in excludeSections:
				allFile.write("\n\n#Service :" + service)
				for property in config[service]:
					if property == 'hostgroup':
						allFile.write("\n" + service + "_hosts: " + str(gethostNameIpMap(globalConfigData[service][property])))
						inventoryMap.append(globalConfigData[service][property])
					else:
						allFile.write("\n" + service + "_" + property + ": " + str(globalConfigData[service][property]))
	allFile.close()


def generateHdpConfigration(hdpConfig):
		generateHdpHostConfig(hdpConfig)
		generateBluePrint(hdpConfig)

def checkHostGroupNameExists(groupName):

	if groupName not in commonHostGroups:
		raise Invalid('Hostgroup \'{0}\' doesn\'t exist\'s in {1}'.format(groupName,commonHostGroups))

	if len(commonHostGroupMap[groupName]) == 0:
		raise Invalid('No hosts mapped to hostgroup \'{0}\' in {1}'.format(groupName,commonHostGroups))



def loadcommonHostgroupInfo(configdata):
	data = configdata.get('common')
	try:
	   validator.common(data)
	except MultipleInvalid as e:
		for error in e.errors:
			log.log(log.LOG_ERROR, "YAML validation Error: message:{0} in {1}".format(error, data.get('common')))
		sys.exit(1)

	hostgroups = data.get('hostgroups')
	for hostgroup in hostgroups:
		  if hostgroup['name'] not in commonHostGroups:
			commonHostGroups[hostgroup['name']] = hostgroup
			commonHostGroupMap[hostgroup['name']] = {}

	for primary_host in data.get('primary_hosts'):
		if primary_host['hostgroup'] not in commonHostGroups:
			raise Invalid('Unknown hostgroup {0} mapped to host {1}'.format(primary_host['hostgroup'],primary_host['name']))
		else:
			if primary_host['ip'] in commonHostGroupIpMap:
				raise Invalid('ip \'{0}\' mapped to two host groups {1} & {2}'.format(primary_host['ip'],commonHostGroupIpMap.get(primary_host['ip']),primary_host['hostgroup']))
			else:
				commonHostGroupIpMap[primary_host['ip']] = primary_host['hostgroup']
			hostGroup = commonHostGroupMap[primary_host['hostgroup']]
			hostGroup[primary_host['ip']] = primary_host
			primary_host['fqdn'] = primary_host['name']+'.'+commonHostGroups[primary_host['hostgroup']].get('domain')
			commonHostGroupIpMap[primary_host.get('ip')] = primary_host['hostgroup']



def updateConfigData(configData,inventoryName1,path1):
	global globalConfigData
	global commonHostGroupIpMap
	global commonHostGroups
	global commonHostGroupMap
	global components
	global oshostConfig
	global inventoryName
	global path
	globalConfigData = configData
	inventoryName = inventoryName1
	path = path1
	commonHostGroups = {}
	commonHostGroupMap = {}
	commonHostGroupIpMap = {}
	components = ['all']
	oshostConfig= {}

def checkifAnyInvalidHostGroupMap():

	 inventoryMap = getInventoryHostgroupMap()
	 for hostgroup in inventoryMap:
		 for section in globalHostGroupsMaps:
			 if section !=inventoryName :
				 sectionConfig = globalHostGroupsMaps[section]
				 if hostgroup in sectionConfig:
					 log.log(log.LOG_ERROR,'Same hostgroup in common[hostgroups] cannot be mapped in multiple clutster sections')
					 log.log(log.LOG_ERROR,'common[hostgroups][name] =  [{0}] is used in Sections {1} and {2}: Please re-check'.format(hostgroup,section,inventoryName))
					 sys.exit(1)

def createInvetoryDirectories():
	fileSeperator = os.sep
	#Create if inventories directory doesnt exists
	invetoriesdir = "{0}{1}inventories".format(path,fileSeperator)
	if not os.path.isdir(invetoriesdir):
		os.makedirs(invetoriesdir)
	global inventorydir
	inventorydir = "{0}{1}{2}".format(invetoriesdir,fileSeperator,inventoryName)
	if not os.path.isdir(inventorydir):
	    os.makedirs(inventorydir)
	groupvarsdir = "{0}{1}{2}".format(inventorydir,fileSeperator,"group-vars")
	if not os.path.isdir(groupvarsdir):
		os.makedirs(groupvarsdir)
	global rolesConfigFilesdir
	rolesConfigFilesdir = "{0}{1}{2}".format(inventorydir,fileSeperator,"roles_config")
	if not os.path.isdir(rolesConfigFilesdir):
		os.makedirs(rolesConfigFilesdir)

	global allConfigFile
	global ansiblehostsfile
	global etchostsFile
	global defaultAllFile


	allConfigFile = "{0}{1}{2}".format(groupvarsdir,fileSeperator,"all")
	ansiblehostsfile ="{0}{1}{2}".format(inventorydir,fileSeperator,'hosts')
	etchostsFile = '{0}{1}{2}'.format(rolesConfigFilesdir,fileSeperator,'host_list')
	defaultAllFile = '{0}{1}{2}{3}{4}'.format(path,fileSeperator,'defaults',fileSeperator,'default-all')


def main(configdata,inventoryName,path):
	updateConfigData(configdata,inventoryName,path)
	createInvetoryDirectories()
	loadcommonHostgroupInfo(configdata)
	hdpConfig = configdata.get('hdp',None)
	if hdpConfig != None:
	   generateHdpConfigration(configdata["hdp"])
	generateCommonDefaultAllConfigFile(configdata)
	generateAnsibleAllFile(configdata,components)
	generateAnsibleHostFile(configdata,components)
	checkifAnyInvalidHostGroupMap()
	generateEtcHostFile(configdata,components)





