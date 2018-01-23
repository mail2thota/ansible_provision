import yaml
import sys
import os
import log
import validatecluster
import configcluster

excludeSections =['common','foreman']


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
     #Validating Each Section
     if len(clusterNames) == 0:
         log.log(log.LOG_ERROR,'Configuration is empty')
         sys.exit(1)
     if validate:
         for clusterName in clusterNames:
            log.log(log.LOG_INFO,'Validating config.yml Section@{0}'.format(clusterName))
            clusterData = getClusterInfo(config,clusterName)
            validatecluster.main(clusterData)
     else:
         log.log(log.LOG_WARN,'Skipping config.yml validation')
     #Creating Config files
     for clusterName in clusterNames:
        log.log(log.LOG_INFO,'Creating config files of section@{0}'.format(clusterName))
        clusterData = getClusterInfo(config,clusterName)
        configcluster.main(clusterData,clusterName,path)

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
        log.log(log.LOG_INFO, "Check if '{0}' is available".format(config_file))
        sys.exit(1)


if __name__ == '__main__':
    main()

