
import yaml
import os
import sys

oshostConfig = {}
ansiblehostsfile = 'hosts'
allConfigFile = 'all'
etchostsFile = 'host_list'
defaultConfigFile= 'config.yml'
defaultAllFile = 'default-all'
globalConfigData =''
def generateHostConfig(hdpHostConfig):
    print "Generating ansible host group configuraiton for hdp cluster"
    hostInfo = []
    hdpHostInfo = {}
    outfile = open(ansiblehostsfile, 'w')
    outfile.write("["+hdpHostConfig["ansible_host_group"]+"]")
    if hdpHostConfig["cluster_type"] == 'single_node':
        print globalConfigData
        if "hosts" in globalConfigData["ambari"]:
             for host in globalConfigData["ambari"]["hosts"]:
                outfile.write("\n" + host["name"])
        else:
            print 'hosts are not specified for the service : ambari'
    else:
        for groupsInfo in hdpHostConfig[hdpHostConfig["cluster_type"]]["host_groups"]:
            for groupName in groupsInfo:
                hosts = groupsInfo[groupName]["hosts"]
                for host in hosts:
                    outfile.write('\n'+host["name"])
                    oshostConfig[host["ip"]] = host["name"]
    return

def generateBluePrint(hdpConfig):
    outfile = open(hdpConfig["cluster_type"]+'.yml', 'w+')

    blueprint = {"cluster_name" : hdpConfig["cluster_name"],"blueprint_name" : hdpConfig["blueprint"], "configurations"  : hdpConfig["blueprint_configuration"]}
    if "default_password" in hdpConfig:
        blueprint["blueprint"] = { "default_password" : hdpConfig["default_password"],"stack_name" : "HDP", "stack_version"  : hdpConfig["stack"], "groups" : []}
    else :
        print "default_password not mentioned in the blue print"
        blueprint["blueprint"] = { "stack_name" : "HDP", "stack_version"  : hdpConfig["stack"], "groups" : []}

    if hdpConfig['cluster_type'] == 'multi_node':
        for groupsInfo in hdpConfig[hdpConfig["cluster_type"]]["host_groups"]:
            components = []
            for groupName in groupsInfo:
                groupInfo = groupsInfo[groupName]
                componentset = groupInfo["components"]
                for componentName in componentset:
                   for component in hdpConfig["component_groups"][componentName]:
                       components.append(component)
            hostslist =  []
            for hostinfo in groupInfo["hosts"]:
                    hostslist.append(hostinfo["name"])
            components = list(set(components))
            blueprint["blueprint"]["groups"].append({"name" : groupName,"cardinality" : groupInfo["cardinality"], "hosts" : hostslist,"components" : components, "configuration" : groupInfo["configuration"]})

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
        blueprint["blueprint"]["groups"].append({"name" : "master-1","cardinality" : 1, "hosts" : hostslist,"components" : components, "configuration" : []})

    yaml.dump(blueprint,outfile,default_flow_style=False, allow_unicode=True)
    print blueprint
    return blueprint


def generateCommonDefaultAllConfigFile(config):
	
    with open(defaultAllFile, 'r') as stream:
        try:
            configdata = yaml.load(stream)
            with open(allConfigFile,'w') as allFile:
                allFile.write("#Generated from default-all file \n")
                for property in configdata:
                        allFile.write("\n"+property+": "+str(configdata[property]))

        except yaml.YAMLError as exc:
            print exc

def generateCommonConfigHostsFile(config):
    fileMode = None
    #Adding the host groups

    hostsGroupFIle = os.path.exists(ansiblehostsfile)
    if hostsGroupFIle:     fileMode = 'a'
    else:                  fileMode = 'w'

    with open(ansiblehostsfile, fileMode) as hostFile:
        for service in config:
            if service == "hdp":
                continue
            #Creating/Updating ansible hosts group file
            if "ansible_host_group" in config[service]:
                if "hosts" in config[service]:
                    print service
                    hostFile.write("\n\n\n[" +config[service]["ansible_host_group"]+"]")
                    for host in config[service]["hosts"]:
                          hostFile.write("\n"+host["name"])
                          if 'ip' in host:
                            oshostConfig[host["ip"]] = host["name"]
                else: print 'hosts are not specified for the service :'+service
            else : print service +" doesn't have ansible host specification properties"
    hostFile.close()

    #Adding the properties to all file
    isAllConfigFileExists = os.path.exists(allConfigFile)
    if isAllConfigFileExists:  fileMode = 'a'
    else:              fileMode = 'w'
    with open(allConfigFile,fileMode) as allFile:
            allFile.write("\n\n\n\n#Generated from config.yaml ")
            for service in config:
                allFile.write("\n\n#Service :"+service)
                for property in config[service]:
                     allFile.write("\n" + service + "_" + property + ": " + str(configdata[service][property]))
    allFile.close()


def generateHdpConfigration(hdpConfig):
    if hdpConfig["cluster_type"] in ["multi_node","single_node"]:
        generateHostConfig(hdpConfig)
        generateBluePrint(hdpConfig)
    else:
        print "cluster_type  must be either multi_node or single_node but configured type is :"+hdpConfig["cluster_type"]
        sys.exit(1);
    return

def addNodeCredentials(configdata):
    print configdata
    if "ansible_ssh" in configdata:
        fileMode = ''
        hostsGroupFile = os.path.exists(ansiblehostsfile)
        if hostsGroupFile: fileMode = 'a'
        else:              fileMode = 'w'
        hostsGroupFIle = open(ansiblehostsfile, fileMode)
        hostsGroupFIle.write("\n\n\n[all:vars]\n")
        hostsGroupFIle.write("ansible_ssh_user="+configdata["ansible_ssh"]["user"]+"\n")
        hostsGroupFIle.write("ansible_ssh_pass="+configdata["ansible_ssh"]["pass"])

    else:
        print "Node Credentials are not provided for ansible to deploy"
        sys.exit(1)
with open(defaultConfigFile, 'r') as stream:
    try:
        configdata = yaml.load(stream)
        globalConfigData = configdata
        #Configuration specific to hdp
        # Generate the host groups
	if 'hdp' in configdata:
        	generateHdpConfigration(configdata["hdp"])
	else:
	  print 'hdp specficiations are not mentioned'

        generateCommonDefaultAllConfigFile(configdata)
	
        generateCommonConfigHostsFile(configdata)
        addNodeCredentials(configdata)

        #Genearating host configuration to suplly ansible-boot
        osHostsFile = open(etchostsFile, 'w')
	for host in oshostConfig:
            osHostsFile.write(host+" "+oshostConfig[host]+"\n")
	
        
	print "all hosts"
	print oshostConfig
    except yaml.YAMLError as exc:
        print(exc)
