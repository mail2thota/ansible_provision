import os
import sys

import yaml

import log
from config_schema import Validator


excludeSections = ['foreman','common']
globalEnvHostGroupMap = {}

globalHostGroupsMaps = {}


def gethosts(groupName):
	hostgroup = envHostGroupsMap[groupName]
	hosts = []
	for host in hostgroup.get('hosts'):
		hosts.append(host['name'])
	return hosts

def gethostNameIpMap(groupName):
	hostgroup = envHostGroupsMap[groupName]
	data = []
	for host in hostgroup.get('hosts'):
		data.append({'ip': host.get('ip',''),'name': host.get('name')})
	return data

def gethostGroupName(serviceName):

    return globalConfigData[serviceName]['hostgroup']

def addToEtcHostsList(groupName):
    hosts = gethostNameIpMap(groupName)
    for host in hosts:
        oshostConfig[host['ip']] = host['name']



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
		for host in gethosts(host_group_name):
			outfile.write("\n" + '{0}'.format(host))
		addToEtcHostsList(host_group_name)

	log.log(log.LOG_INFO, "{0}: Created ansible hdp host group configuration file : hosts".format(clustername))

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
	log.log(log.LOG_INFO, "{0}: blueprint: {1}".format(clustername,str(blueprint)))
	return blueprint


def generateCommonDefaultAllConfigFile(config):
    filePath = defaultAllFile
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
	log.log(log.LOG_INFO, '{0}: Generated ip & hostname map file to replace  /etc/hosts in all nodes : host_list'.format(clustername))

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
	 log.log(log.LOG_INFO, '{0}: updated ansible hosts file for non hdp components: hosts'.format(clustername))

def generateAnsibleAllFile(config,services):
	fileMode = None
	# Adding the properties to all file

	isAllConfigFileExists = os.path.exists(allConfigFile)
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
					else:
						allFile.write("\n" + service + "_" + property + ": " + str(globalConfigData[service][property]))
	allFile.close()


def generateHdpConfigration(hdpConfig):
		generateHdpHostConfig(hdpConfig)
		generateBluePrint(hdpConfig)



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


def updateConfigData(configData,inventoryName1,path1):
	global globalConfigData
	global components
	global oshostConfig
	global inventoryName
	global path
	global envHostGroupsMap
	global globalEnvHostGroupMap
	envHostGroupsMap = {}
	globalConfigData = configData
	inventoryName = inventoryName1
	path = path1
	components = ['all']
	oshostConfig= {}



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
	groupvarsdir = "{0}{1}{2}".format(inventorydir,fileSeperator,"group_vars")
	if not os.path.isdir(groupvarsdir):
		os.makedirs(groupvarsdir)
	global rolesConfigFilesdir
	rolesConfigFilesdir = "{0}{1}{2}{3}{4}".format(path,fileSeperator,"roles_config",fileSeperator,inventoryName)
	if not os.path.isdir(rolesConfigFilesdir):
		os.makedirs(rolesConfigFilesdir)

	global allConfigFile
	global ansiblehostsfile
	global etchostsFile
	global defaultAllFile
	global envHostGroupsMap
	global globalEnvHostGroupMap
	envHostGroupsMap = {}


	allConfigFile = "{0}{1}{2}".format(groupvarsdir,fileSeperator,"all")
	ansiblehostsfile ="{0}{1}{2}".format(inventorydir,fileSeperator,'hosts')
	etchostsFile = '{0}{1}{2}'.format(rolesConfigFilesdir,fileSeperator,'host_list')
	defaultAllFile = "C:\\cygwin64\\home\\Stelaprolu\\mdr\\mdr_platform_bare_metal\\ansible\\mdr_cluster\\roles\\pre-config\\defaults\\default-all"
	#defaultAllFile = '{0}{1}{2}{3}{4}'.format(path,fileSeperator,'defaults',fileSeperator,'default-all')


def main(configdata,clustername1,path,envHostMap):
	global clustername
	clustername = clustername1
	updateConfigData(configdata,clustername,path)
	createInvetoryDirectories()
	loadEnvSpecificHostgroups(configdata, clustername, envHostMap)
	hdpConfig = configdata.get('hdp')
	if hdpConfig != None:
	   generateHdpConfigration(configdata["hdp"])
	generateCommonDefaultAllConfigFile(configdata)
	generateAnsibleAllFile(configdata,components)
	generateAnsibleHostFile(configdata,components)
	generateEtcHostFile(configdata,components)





