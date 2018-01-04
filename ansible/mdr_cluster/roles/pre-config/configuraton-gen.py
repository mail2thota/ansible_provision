import yaml
import os
import sys
import log
from config_schema import Validator
from error import MultipleInvalid,DictInvalid
from error import MatchInvalid,Invalid

oshostConfig = {}
ansiblehostsfile = 'hosts'
allConfigFile = 'all'
etchostsFile = 'host_list'
defaultConfigFile = 'config.yml'
defaultAllFile = 'default-all'
globalConfigData = ''
validator = Validator()
commonHostGroups = {}
commonHostGroupMap = {}
commonHostGroupIpMap = {}
components = ['all']

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
            for host in gethosts(host_group_name):
                outfile.write("\n" + '{0}'.format(host))
            addToEtcHostsList(host_group_name)

    log.log(log.LOG_INFO, "Create ansible hdp host group configuration file : hosts")

def generateBluePrint(hdpConfig):
    outfile = open(hdpConfig["cluster_type"] + '.yml', 'w+')

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
                        log.log(log.LOG_ERROR,'hdp: Tried to use the non existance component group ['+componentName+"] in hdp[host_groups]["+groupName+"] Please check and re-run")
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
    log.log(log.LOG_INFO,"blueprint: "+ str(blueprint))
    return blueprint


def generateCommonDefaultAllConfigFile(config):

    with open(defaultAllFile, 'r') as stream:
        try:
            configdata = yaml.load(stream)
            with open(allConfigFile, 'w') as allFile:
                allFile.write("#Generated from default-all file \n")
                for property in configdata:
                    allFile.write("\n" + property + ": " + str(configdata[property]))
        except yaml.YAMLError as exc:
            log.log(log.LOG_ERROR,"Unalbe to write the all file" +exc)
            sys.exit(1)
    log.log(log.LOG_INFO, 'Generated ansible all file : config.yml')

def generateEtcHostFile(config,services):
    osHostsFile = open(etchostsFile, 'w')
    for host in oshostConfig:
        osHostsFile.write(host + " " + oshostConfig[host] + "\n")
    log.log(log.LOG_INFO,'Generated ip & hostname map file to replace  /etc/hosts in all nodes : host_list')

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

    if isAllConfigFileExists:
        fileMode = 'a'
    else:
        fileMode = 'w'
    with open(allConfigFile, fileMode) as allFile:
        allFile.write("\n\n\n\n#Generated from config.yaml ")
        for service in config:
            allFile.write("\n\n#Service :" + service)
            for property in config[service]:
                if property == 'hostgroup':
                    allFile.write("\n" + service + "_hosts: " + str(gethostNameIpMap(configdata[service][property])))
                else:
                    allFile.write("\n" + service + "_" + property + ": " + str(configdata[service][property]))
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
            log.log(log.LOG_ERROR, "YAML validation Error: message:{0} in {1}".format(error,data.get('common')))
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
                    log.log(log.LOG_ERROR, "YAML validation Error: message:{0} in {1}".format(error,hostgroup))
                sys.exit(1)
            except Invalid as e:
                log.log(log.LOG_ERROR, "YAML validation Error: message:{0} in {1}".format(e, hostgroup))
                sys.exit(1)

    for primary_host in data.get('primary_hosts'):
        try:
            validator.common_primary_host(primary_host)
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
        except Invalid as e:
            log.log(log.LOG_ERROR, "YAML validation Error: common[primary_hosts]:{0} in {1}".format(e, primary_host))
            sys.exit(1)


def validateConfigFile(configdata):


    try:
       validator.config( configdata)
       if 'hdp' or 'ambari' in configdata:
           validator.hdpambari(configdata)
    except MultipleInvalid as e:
        for error in e.errors:
            log.log(log.LOG_ERROR, "YAML validation Error: message:{0} in {1}".format(error,configdata))
        sys.exit(1)

    try:
        for configService in configdata:
                serviceData = configdata.get(configService)
                msg = 'Success'
                msglevel = log.LOG_INFO_RM

                if configService == 'default':
                    validator.default(serviceData)

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
                           log.log(log.LOG_ERROR, configService +": component_groups[" +component_group+"] : YAML validation Error: {0} in  {1}".format(exe.error_message,component_groups.get(component_group)))
                           sys.exit(1)

                    host_groups = serviceData.get('hostgroups')
                    for host_group  in host_groups:
                        host_group_name = host_group.keys()[0]
                        try:
                            validator.host_group(host_group[host_group_name])
                            checkHostGroupNameExists(host_group[host_group_name]['hostgroup'])
                        except Invalid as exe:
                            log.log(log.LOG_ERROR,
                                    configService + ": hostgroups["+host_group_name+"][hostgroup] : YAML validation Error: {0} in  {1}".format(
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

                elif configService == 'es_node':
                    validator.es_node(serviceData)
                    checkHostGroupNameExists(serviceData.get('hostgroup'))

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

                log.log(log.LOG_INFO, 'Yaml validation : {0}  {1}!'.format(configService,log.log(msglevel,msg)))

    except MultipleInvalid as e:
        for error in e.errors:
           log.log(log.LOG_ERROR,configService+" : YAML validation Error:{0} in {1}".format(error,configdata[configService]))
        sys.exit(1)
    except MatchInvalid as e:
        log.log(log.LOG_ERROR,
                configService + " : YAML validation Error:{0} in {1}".format(e.error_message, configdata[configService]))
        sys.exit(1)
    except Invalid as e:
        log.log(log.LOG_ERROR,
                configService + " : YAML validation Error:{0} in {1}".format(e.error_message,configdata[configService]))
        sys.exit(1)



with open(defaultConfigFile, 'r') as stream:
    try:
        print str(sys.argv)
        configdata = yaml.load(stream)
        globalConfigData = configdata

        loadcommonHostgroupInfo(configdata)

        validateConfigFile(configdata)

        generateHdpConfigration(configdata["hdp"])

        generateCommonDefaultAllConfigFile(configdata)

        generateAnsibleAllFile(configdata,components)
        generateAnsibleHostFile(configdata,components)
        generateEtcHostFile(configdata,components)

    except yaml.YAMLError as exc:
        log.log(log.LOG_ERROR,exc)
        sys.exit(1)
