import yaml
import sys
import os
import log
import json
try:
    import requests
except ImportError:
    REQUESTS_FOUND = False
else:
    REQUESTS_FOUND = True


ambari_url = ''


def get(ambari_url, user, password, path):
    r = requests.get(ambari_url + path, auth=(user, password))
    return r

def getambariUrl(configData):

    return "http://"+str(configData['ambari']['host'])+":"+str(configData["ambari"]["port"])+"/api/v1/"

 
def gethostList(configData):
    path = 'clusters/'+configData['ambari']['clustername']+"/hosts"
   
    response = get(getambariUrl(configData),configData['ambari']['user'],configData['ambari']['password'],path)
    if response.status_code != 200:
        log.log(log.LOG_ERROR,'couldn\'t able to connect to ambari server : {0}'.format(response.content))
        sys.exit(1)

    hostinfo = json.loads(response.content)['items']  
    hdphosts = open('hdp_host_list', 'w')
    for host in hostinfo:
        print host['Hosts']['host_name']
        hdphosts.write(host['Hosts']['host_name']+'\n')
    log.log(log.LOG_INFO,'Writing all the hosts to file : hdp_host_list')

def main():

    config_file = ''
    if os.path.isfile(sys.argv[1]):
        config_file = sys.argv[1]
    else:
        log.log(log.LOG_ERROR,"Please suply the update_hdp_cluster.yml")
        log.log(log.LOG_ERROR, "No YAML provided")
        sys.exit(1)
    try:
        config_file = open(config_file, 'r')
        try:
            config = yaml.load(config_file)
         
	    gethostList(config)
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

