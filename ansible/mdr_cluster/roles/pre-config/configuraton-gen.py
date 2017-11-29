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

def generateHostConfig(hdpHostConfig):
    log.log(log.LOG_INFO,"Generating ansible host group configuraiton for hdp cluster")
    hostInfo = []
    hdpHostInfo = {}
    outfile = open(ansiblehostsfile, 'w')
    outfile.write("[hdp_hosts]")
    if hdpHostConfig["cluster_type"] == 'single_node':
        if "hosts" in globalConfigData["ambari"]:
            for host in globalConfigData["ambari"]["hosts"]:
                outfile.write("\n" + host["name"])
        else:
            log.log(log.LOG_ERROR, 'hosts are not specified for the service : ambari')
    else:
        for groupsInfo in hdpHostConfig[hdpHostConfig["cluster_type"]]["host_groups"]:
            for groupName in groupsInfo:
                hosts = groupsInfo[groupName]["hosts"]
                for host in hosts:
                    outfile.write('\n' + host["name"])
                    if 'ip' in host:
                        oshostConfig[host["ip"]] = host["name"]
    return


def generateBluePrint(hdpConfig):
    outfile = open(hdpConfig["cluster_type"] + '.yml', 'w+')

    blueprint = {"cluster_name": hdpConfig["cluster_name"], "blueprint_name": hdpConfig["blueprint"],
                 "configurations": hdpConfig["blueprint_configuration"]}
    if "default_password" in hdpConfig:
        blueprint["blueprint"] = {"default_password": hdpConfig["default_password"], "stack_name": "HDP",
                                  "stack_version": hdpConfig["stack"], "groups": []}
    else:
        log.log(log.LOG_WARN, "default_password not mentioned in the blue print")
        blueprint["blueprint"] = {"stack_name": "HDP", "stack_version": hdpConfig["stack"], "groups": []}

    if hdpConfig['cluster_type'] == 'multi_node':
        for groupsInfo in hdpConfig[hdpConfig["cluster_type"]]["host_groups"]:
            components = []
            for groupName in groupsInfo:
                groupInfo = groupsInfo[groupName]
                componentset = groupInfo["components"]
                for componentName in componentset:
                    if componentName  not in hdpConfig['component_groups']:
                        log.log(log.LOG_ERROR,'Tried to use the non existance component group ['+componentName+"] in hdp[multi_node][host_groups]["+groupName+"] Please specify existing one")
                        sys.exit(1)
                    for component in hdpConfig["component_groups"][componentName]:
                        components.append(component)
            hostslist = []
            for hostinfo in groupInfo["hosts"]:
                hostslist.append(hostinfo["name"])
            components = list(set(components))
            blueprint["blueprint"]["groups"].append(
                {"name": groupName, "cardinality": groupInfo.get("cardinality",1), "hosts": hostslist,
                 "components": components, "configuration": groupInfo.get("configuration",[])})

    elif hdpConfig['cluster_type'] == 'single_node':
        components = []
        for component in hdpConfig["component_groups"]:
            componentInfo = hdpConfig["component_groups"][component]
            for componentName in componentInfo:
                components.append(componentName)
        components = list(set(components))

        hostslist = []
        for hostinfo in globalConfigData['ambari']['hosts']:
            hostslist.append(hostinfo["name"])
        blueprint["blueprint"]["groups"].append(
            {"name": "master-1", "cardinality": 1, "hosts": hostslist, "components": components, "configuration": []})

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


def generateCommonConfigHostsFile(config):
    fileMode = None
    # Adding the host groups

    hostsGroupFIle = os.path.exists(ansiblehostsfile)
    if hostsGroupFIle:
        fileMode = 'a'
    else:
        fileMode = 'w'

    with open(ansiblehostsfile, fileMode) as hostFile:
        for service in config:
            if service == "hdp":
                continue
            # Creating/Updating ansible hosts group file
            if "hosts" in config[service]:
                hostFile.write("\n\n\n[" + service + "_hosts]")
                for host in config[service]["hosts"]:
                    hostFile.write("\n" + host["name"])
                    if 'ip' in host:
                        oshostConfig[host["ip"]] = host["name"]
            else:
                log.log(log.LOG_WARN,'hosts are not specified for the service :' + str(service))
    hostFile.close()

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
                allFile.write("\n" + service + "_" + property + ": " + str(configdata[service][property]))
    allFile.close()


def generateHdpConfigration(hdpConfig):
    if hdpConfig["cluster_type"] in ["multi_node", "single_node"]:
        generateHostConfig(hdpConfig)
        generateBluePrint(hdpConfig)
    else:
        log.log(log.LOG_ERROR, "cluster_type  must be either multi_node or single_node but configured type is :" + hdpConfig[
            "cluster_type"])
        sys.exit(1);
    return


def addNodeCredentials(configdata):
    if "ansible_ssh" in configdata:
        fileMode = ''
        hostsGroupFile = os.path.exists(ansiblehostsfile)
        if hostsGroupFile:
            fileMode = 'a'
        else:
            fileMode = 'w'
        hostsGroupFIle = open(ansiblehostsfile, fileMode)
        hostsGroupFIle.write("\n\n\n[all:vars]\n")
        hostsGroupFIle.write("ansible_ssh_user=" + configdata["ansible_ssh"]["user"] + "\n")
        hostsGroupFIle.write("ansible_ssh_pass=" + configdata["ansible_ssh"]["pass"])

    else:
        log.log(log.LOG_ERROR, "Node Credentials are not provided for ansible to deploy")
        sys.exit(1)


def validateHosts(configService,data):
    hosts= data.get('hosts')
    for host in hosts:
        try:
            validator.host(host)
        except MultipleInvalid as exe:
            log.log(log.LOG_ERROR,
                    configService + "[hosts] : YAML validation Error: {0} in  {1}".format(
                        exe.error_message, host))
            sys.exit(1)

def validateConfigFile(configdata):

    #Validating madatory ansible_ssh section
    try:
       validator.config( configdata)

    except MultipleInvalid as e:
        for error in e.errors:
            log.log(log.LOG_ERROR, "YAML validation Error: message:{0} in {1}".format(error,configdata))
        sys.exit(1)

    try:
        for configService in configdata:
                if configService == 'ansible_ssh':
                   validator.ansible_ssh(configdata.get('ansible_ssh'))
                elif configService == 'default':
                    validator.default(configdata.get(configService))
                elif configService == 'ambari':
                    validator.ambari(configdata.get(configService))
                    #Verify ambari must have hosts if not it will fail
                    validateHosts(configService,configdata.get(configService))

                elif configService == 'hdp':
                    #Single level varaibles validation
                    validator.hdp(configdata.get(configService))
                    component_groups = configdata.get(configService).get('component_groups')
                    #Check the each component group for unique elemements
                    for component_group in component_groups :
                        try:
                            validator.component_group(component_groups.get(component_group))
                        except Invalid as exe:
                           log.log(log.LOG_ERROR, configService +": component_groups[" +component_group+"] : YAML validation Error: {0} in  {1}".format(exe.error_message,component_groups.get(component_group)))
                           sys.exit(1)

                    #Validating host groups recursively
                    host_groups = configdata.get(configService).get('multi_node').get('host_groups')
                    for host_group  in host_groups:
                        host_group_name = host_group.keys()[0]
                        try:
                            validator.host_group(host_group.get(host_group_name))
                            hosts = host_group.get(host_group_name).get('hosts')
                            for host in hosts:
                                try:
                                  validator.host(host)
                                except MultipleInvalid as exe:
                                    log.log(log.LOG_ERROR,
                                            configService + ": host_groups["+host_group_name+"][hosts] : YAML validation Error: {0} in  {1}".format(
                                                exe.error_message, host))
                                    sys.exit(1)
                        except MultipleInvalid as exe:
                            log.log(log.LOG_ERROR,
                                    configService + ": host_groups["+host_group_name+"][hosts] : YAML validation Error: {0} in  {1}".format(
                                        exe.error_message, host_group))
                            sys.exit(1)
                elif configService == 'hdp_test':
                        validator.hdp_test(configdata.get(configService))
                        validateHosts(configService, configdata.get(configService))
                elif configService == 'kibana':
                        validator.kibana(configdata.get(configService))
                        validateHosts(configService, configdata.get(configService))
                else:
                        validator.generic(configdata.get(configService))
                        validateHosts(configService, configdata.get(configService))



    except (MultipleInvalid)as e:
        for error in e.errors:
           log.log(log.LOG_ERROR,configService+" : YAML validation Error:{0} in {1}".format(error,configdata[configService]))
        sys.exit(1)
    except MatchInvalid as e:
        log.log(log.LOG_ERROR,
                configService + " : YAML validation Error:{0} in {1}".format(e.error_message, configdata[configService]))
        sys.exit(1)
    except Invalid as e:
        log.log(log.LOG_ERROR,
                configService + " : YAML validation Error:{0} in {1}".format(e.error_message,
                                                                             configdata[configService]))
        sys.exit(1)



with open(defaultConfigFile, 'r') as stream:
    try:
        configdata = yaml.load(stream)
        globalConfigData = configdata
        validateConfigFile(configdata)
        # Configuration specific to hdp
        # Generate the host groups
        if 'hdp' in configdata:
            generateHdpConfigration(configdata["hdp"])
        else:
            log.log(log.LOG_INFO,'Hdp Specification is not mentioned')

        generateCommonDefaultAllConfigFile(configdata)

        generateCommonConfigHostsFile(configdata)
        addNodeCredentials(configdata)

        # Genearating host configuration to suplly ansible-boot
        osHostsFile = open(etchostsFile, 'w')
        for host in oshostConfig:
        # retriving current host
            osHostsFile.write(host + " " + oshostConfig[host] + "\n")
        # retriving current host
    except yaml.YAMLError as exc:
        print exc
        sys.exit(1)

