import yaml
import sys
import os
import log
import validatecluster
import configcluster
from config_schema import Validator
from error import MatchInvalid,Invalid
from error import MultipleInvalid



validator = Validator()
excludeSections =['common','foreman']

hostnameswithtags = { }

def getClusters(config):

     clusterNames = []
     for clustername in config:
           if clustername not in excludeSections:
              clusterNames.append(clustername)
     return clusterNames

def getCommonConfig(config):
     defaultConfig = {}
     for section in config:
      if section in excludeSections:
           defaultConfig[section] = config.get(section,{})
     return  defaultConfig


def getClusterInfo(config,section):
    clusterInfo = config[section]
    for excludeSection in excludeSections:
        clusterInfo[excludeSection] = config.get(excludeSection,{})

    return clusterInfo





def configNewClusters(config,path,validate):
     commonConfig = getCommonConfig(config)
     clusterNames = getClusters(config)
     envHostMap = createGlobalHostGroupmap(config)
     globalEnvHostGroupMap = {}
     #Validating Each Section
     if len(clusterNames) == 0:
         log.log(log.LOG_ERROR,'Configuration is empty')
         sys.exit(1)
     if validate:
         for clusterName in clusterNames:
            log.log(log.LOG_INFO,'Validating config.yml Section@{0}'.format(clusterName))
            clusterData = getClusterInfo(config,clusterName)
            globalEnvHostGroupMap = validatecluster.main(clusterData,clusterName,envHostMap)

     else:
         log.log(log.LOG_WARN,'Skipping config.yml validation')
     #Check for hostshared with different tags
     for hostname  in hostnameswithtags:
         envConflictMap = {}
         hosttags = hostnameswithtags[hostname]
         for hostag in hosttags:
             for envName in globalEnvHostGroupMap:
                 if hostag in globalEnvHostGroupMap[envName]:
                      envConflictMap[envName] = hostag

         if len(envConflictMap) > 1:
             log.log(log.LOG_ERROR,'Not Allowed: host[{0}] is shared betweeen environments {1}  with hostgroups/tags {2}'.format(hostname,envConflictMap.keys(),envConflictMap.values()))
             sys.exit(1)

     #Creating Config files
     for clusterName in clusterNames:
        log.log(log.LOG_INFO,'Creating config files of section@{0}'.format(clusterName))
        clusterData = getClusterInfo(config,clusterName)
        configcluster.main(clusterData,clusterName,path,envHostMap)

def createInventoriesListFile(config,path):
    filePath = "{0}{1}{2}".format(path,os.sep,'inventory_list')
    with open(filePath, 'w') as fileData:
        try:
             invetoryNames = getClusters(config)
             for inventory in invetoryNames:
                 fileData.write("{0}{1}".format(inventory,"\n"))
        except yaml.YAMLError as exc:
            log.log(log.LOG_ERROR, "Unalbe to write the Invetories list file" + exc)
            sys.exit(1)


def validatePreRequistives(configdata):
    commonData = configdata.get('common')
    try:
        validator.common(commonData)
    except MultipleInvalid as e:
        for error in e.errors:
            log.log(log.LOG_ERROR, "common validation Error: message:{0} in {1}".format(error, commonData))
        sys.exit(1)

    hostgroups = commonData.get('hostgroups')

    # Checking host group static data structure
    for hostgroup in hostgroups:
        try:
            validator.common_hostgroup(hostgroup)
        except MultipleInvalid as e:
            for error in e.errors:
                log.log(log.LOG_ERROR,
                        "Common[hostsgroups] validation Error: message:{0} in {1}".format(error, hostgroup))
            sys.exit(1)
        except Invalid as e:
            log.log(log.LOG_ERROR, "Common[hostgroups] validation Error: message:{0} in {1}".format(e, hostgroup))
            sys.exit(1)

    # Validating Primary Hosts
    for primary_host in commonData.get('primary_hosts'):
        try:
            validator.common_primary_host(primary_host)
        except MultipleInvalid as e:
            for error in e.errors:
                log.log(log.LOG_ERROR,
                        "Common[primary_hosts] validation Error: message:{0} in {1}".format(error, primary_host))
            sys.exit(1)
        except Invalid as e:
            log.log(log.LOG_ERROR, "Common[primary_hosts] validation Error: message:{0} in {1}".format(e, primary_host))
            sys.exit(1)

def createGlobalHostGroupmap(configdata):
    validatePreRequistives(configdata)
    global  groupsMap
    groupsMap = {'hostgroups': {},'tags':{}}
    hostGroupsMap = groupsMap['hostgroups']
    commonData = configdata.get('common',{})

    #Map based on Hostgroup
    for hostgroup in commonData.get('hostgroups',{}):
        hostgroupName  = hostgroup['name']
        if hostgroupName not in hostGroupsMap:
            hostGroupsMap[hostgroupName] = { 'hosts':[],'domain':hostgroup['domain']}
        else:
            log.log(log.LOG_ERROR,'Common[hostgroups]: Validation Error Duplicate host group name : {0}'.format(hostgroupName))
            sys.exit(1)

    #Added to hostgroup and create tag group if doesnt exists and map ip to it
    tagsHostsGroupMap = groupsMap.get('tags')
    ipmap = {}
    hostnamemap = {}

    for primary_host in commonData['primary_hosts']:
        hostgroupName = primary_host['hostgroup']
        name = primary_host['name']
        ip = primary_host.get('ip')
        #Check if any ip reuse
        if (ip not in ipmap) or (ip is None):
            ipmap[ip] = name
        elif ip is not None:
            log.log(log.LOG_ERROR,"Common[primary_hosts] Config validation Error : {0} is mapped to two hosts {1} and {2}".format(ip,ipmap[ip],name) )
            sys.exit(1)
        #Check of hostname resuse
        if name not in hostnamemap:
            hostnamemap[name] = ip
        else:
            log.log(log.LOG_ERROR,"Common[primary_hosts] Config validation Error : Duplicate hostname : {0}".format(name))
            sys.exit(1)

        domain =  hostGroupsMap.get(hostgroupName).get('domain')
        host = { 'name' :  "{0}.{1}".format(name,domain) , 'ip' : ip,'user':'','pass': ''}
        hostGroupsMap[hostgroupName]['hosts'].append(host)
        Allgroups = [hostgroupName]

        tags = list(set(primary_host.get('tags',[])))



        for tag in tags:
             Allgroups.append(tag)
             if tag in hostGroupsMap:
                  log.log(log.LOG_ERROR,'Not Allowed: tag and hostgroup name cannot be same: [{0}] '.format(tag))
                  sys.exit(1)
             if tag not in tagsHostsGroupMap:
                 #Create as tag group if doesn't exists
                 tagsHostsGroupMap[tag] =  { 'hosts': []}
                 #Append host with ip to tag group
             taghost = {'name': "{0}.{1}".format(name, domain), 'ip': ip, 'user': '', 'pass': ''}
             tagsHostsGroupMap[tag]['hosts'].append(taghost)
        hostnameswithtags[name] = Allgroups
    return groupsMap

def main():
    config_file = ''
    path= ''
    validate = True
    if os.path.isfile(sys.argv[1]):
        config_file = sys.argv[1]

    else:
        log.log(log.LOG_ERROR, "Please supply config.yml file")
        log.log(log.LOG_ERROR, "No YAML provided")
        sys.exit(1)

    if os.path.isdir(sys.argv[2]):
        path  = sys.argv[2]

    else:
        log.log(log.LOG_ERROR,"Invalid directory ".format(sys.argv[2]))
        sys.exit(1)
    
    if len(sys.argv) == 4:
        validate = sys.argv[3]
    try:
        config_file = open(config_file, 'r')
        try:
            config = yaml.load(config_file)

            configNewClusters(config,path,validate)
            createInventoriesListFile(config,path)

        except yaml.YAMLError, exc:
            log.log(log.LOG_ERROR, "Failed to load/parse import config.yml file, Error:'{0}'".format(exc))
            log.log(log.LOG_INFO, "Check if '{0}' formatted correctly".format(config_file))
            sys.exit(1)
        config_file.close()
    except IOError as e:
        log.log(log.LOG_ERROR, "Failed to open/load import config YAML Error:'{0}'".format(e))
        sys.exit(1)


if __name__ == '__main__':
    main()

