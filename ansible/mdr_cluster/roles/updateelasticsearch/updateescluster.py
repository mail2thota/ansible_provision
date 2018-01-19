import yaml
import sys
import os
import log
import json
import time
try:
    import requests
except ImportError:
    REQUESTS_FOUND = False
else:
    REQUESTS_FOUND = True


es_url = ''

def get(es_url, user, password, path):
    r = requests.get(es_url + path)
    return r

def post(es_url,  path, data):
    r = requests.post(es_url + path, data=data)
    return r

def delete(es_url, path):
    r = requests.delete(es_url + path)
    return r

def put(es_url, path, data):
    r = requests.put(es_url + path, data=data, timeout=1800)
    return r

def getesUrl(configData):

    return "http://"+str(configData["es_master"]["host"])+":"+str(configData["es_master"].get("port","9200"))+"/"
   

def main(): 
    config_file = ''
    if os.path.isfile(sys.argv[1]):
        config_file = sys.argv[1]
    else:
        log.log(log.LOG_ERROR,"Please suply the update_es_cluster.yml")
        log.log(log.LOG_ERROR, "No YAML provided")
        sys.exit(1)
    try:
        config_file = open(config_file, 'r')
        try:
            config = yaml.load(config_file)
            #addHosts(config)   
            #removeHosts(config)     
        except yaml.YAMLError, exc:
            log.log(log.LOG_ERROR, "Failed to load/parse import config YAML, Error:'{0}'".format(exc))
            log.log(log.LOG_INFO, "Check if '{0}' formatted correctly".format(config_file))
            sys.exit(1)
        config_file.close()
    except IOError as e:
        log.log(log.LOG_ERROR, "Failed to open/load import config YAML Error:'{0}'".format(e))
        log.log(log.LOG_INFO, "Check if '{0}' is available".format(config_file))
        sys.exit(1)


if __name__ == '__main__':
    main()

