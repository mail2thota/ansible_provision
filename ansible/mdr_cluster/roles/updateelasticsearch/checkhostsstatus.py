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
esNewHosts = []
esHosts = []

def get(es_url, path):
    try:	
       r = requests.get(es_url + path)
       return r
    except Exception as e:
         log.log(log.LOG_ERROR,'Not able to connect to ES Master Node@{0} Reason : {1}'.format(es_url,e))
         sys.exit(1)

def post(es_url,  path, data):
    try:
       r = requests.post(es_url + path, data=data)
       return r
    except Exception as e:
        log.log(log.LOG_ERROR,'Not able to connect to ES Master Node@{0} Reason : {1}'.format(es_url,e))
        sys.exit(1)

def delete(es_url, path):
    try:    
       r = requests.delete(es_url + path)
       return r
    except Exception as e:
         log.log(log.LOG_ERROR,'Not able to connect to ES Master Node@{0} Reason : {1}'.format(es_url,e))
         sys.exit(1)

def put(es_url, path, data):
    try:
       r = requests.put(es_url + path, data=data, timeout=1800)
       return r
    except Exception as e:
         log.log(log.LOG_ERROR,'Not able to connect to ES Master Node@{0} Reason : {1}'.format(es_url,e))
         sys.exit(1)

def getesUrl(configData):

    return "http://"+str(configData["es_master"]["host"])+":"+str(configData["es_master"].get("port","9200"))+"/"
   
def getClusterHosts(configdata):

   esHosts = list()
   path = '_cat/nodes?format=json'
   r = get(getesUrl(configdata), path)
   if r.status_code == 200 :
       hosts = json.loads(r.content)
       for host in hosts:
                esHosts.append(host['name'])
       return esHosts;
   else:
     log.log(log.LOG_ERROR,'Unable to retrive hosts from es_master host :{0}'.format(r.content))
     sys.exit(1)


def loadHosts(configData):

   hosts = configData.get('es_node').get('add',None)

   if hosts is None or hosts.get('hosts',None) is None:
     log.log(log.LOG_INFO,'No new hoss to check status')
     return
   
   if len(hosts['hosts']) == 0:
        log.log(log.LOG_WARN,'add hosts are 0 Skipping')
        return
   for host in hosts['hosts']:
        esNewHosts.append(host['name']) 


def checkStatusOfNewHosts(configData):
    loadHosts(configData)
    noOfRetries = 5
    attempt = 1 
    addedHosts = list()

    while noOfRetries > 0:
        esHosts = getClusterHosts(configData)
        for host in addedHosts:
           esNewHosts.remove(host) 
        addedHosts = list()      
        for host in esNewHosts:
            if host in esHosts and (host not in addedHosts):   
                log.log(log.LOG_INFO,'{0} added/exists in cluster'.format(host))
                addedHosts.append(host)
            else:
                log.log(log.LOG_INFO,'waiting for {0} to show up in es cluster'.format(host))
           
        if len(esNewHosts) > 0:
          time.sleep(5)
          noOfRetries = noOfRetries-1
          attempt = attempt+1
        else:
          return

    if len(esNewHosts) - len(addedHosts) > 0:

       for host in esNewHosts:
              if host not in addedHosts:
	         log.log(log.LOG_ERROR,'Timedout {0} to showed up cluster,'.format(host))
                      


def decommissionHosts(config):

   path = '_cluster/settings'
   body = json.dumps({ "persistent" :{ "cluster.routing.allocation.exclude._host" : "{0}"}})
   hosts = config.get('es_node').get('remove',None)
   if hosts is None:
     log.log(log.LOG_INFO,'Decommision hosts are empty skipping')
     return


   if 'hosts' in hosts:
     if len(hosts['hosts']) == 0:
        log.log(log.LOG_WARN,'add hosts are empty')
        return
     for host in hosts['hosts']:
       body = json.dumps({ "persistent" :{ "cluster.routing.allocation.exclude._host" : "{0}".format(host['name'])}})
       r =  put(getesUrl(config), path,body) 
       response = json.dumps(r.content)
       if r.status_code in [200]:
            
             log.log(log.LOG_INFO,'decommision response {0}'.format(str(response)))
             log.log(log.LOG_INFO,'Please wait all the shards are reallocated as per sharding stragey and then manually remove shutdown the node : {0}'.format(host['name']))

       else:
         log.log(log.LOG_ERROR,'Failed to submit decommision request {0}'.format(str(response)))
  
   

         


  



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
            checkStatusOfNewHosts(config) 
            decommissionHosts(config)      
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

