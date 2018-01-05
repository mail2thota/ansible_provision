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


ambari_url = ''
ambari_password = ''
ambari_user =''

def get(ambari_url, user, password, path):
    r = requests.get(ambari_url + path, auth=(user, password))
    return r

def post(ambari_url, user, password, path, data):
    headers = {'X-Requested-By': 'ambari'}
    r = requests.post(ambari_url + path, data=data, auth=(user, password), headers=headers)
    return r

def delete(ambari_url, user, password, path):
    headers = {'X-Requested-By': 'ambari'}
    r = requests.delete(ambari_url + path, auth=(user, password), headers=headers)
    return r

def put(ambari_url, user, password, path, data):
    headers = {'X-Requested-By': 'ambari'}
    r = requests.put(ambari_url + path, data=data, auth=(user, password), headers=headers, timeout=1800)
    return r

def getambariUrl(config): 

    return "http://"+str(config['ambari']['host'])+":"+str(config["ambari"]["port"])+"/api/v1/"


def get_request_status(ambari_url, user, password, cluster_name, request_id):
    path = 'clusters/{0}/requests/{1}'.format(cluster_name, request_id)
    r = get(ambari_url, user, password, path)
    if r.status_code != 200:
        msg = 'Could not get cluster request status: request code {0}, \
                    request message {1}'.format(r.status_code, r.content)
        raise Exception(msg)
    service = json.loads(r.content)
    return service['Requests']['request_status']


def wait_for_request_complete(ambari_url, user, password, cluster_name, request_id, sleep_time):
    time.sleep(sleep_time)
    while True:
        status = get_request_status(ambari_url, user, password, cluster_name, request_id)
        if status == 'COMPLETED':
            return status
        elif status in ['FAILED', 'TIMEDOUT', 'ABORTED', 'SKIPPED_FAILED']:
            return status
        else:
            time.sleep(sleep_time)

def addhost2group(host,hostgroup,configdata):
    hdp = configdata['hdp'] 
    bodydata = json.dumps({"blueprint": "{0}".format(hdp['blueprint']), "host_group" : "{0}".format(hostgroup) })
    path = 'clusters/'+hdp['clustername']+'/hosts/'+host
    r = post(getambariUrl(configdata),getCredentials(configdata,'user'), getCredentials(configdata,'password'), path, bodydata)
    return r

def getDataNodeCount(configdata):
    path = 'clusters/'+configdata['hdp']['clustername']+'/components/DATANODE'
    r = get(getambariUrl(configdata),getCredentials(configdata,'user'), getCredentials(configdata,'password'), path)
   
    if r.status_code == 200:
        host_components = json.loads(r.content)['host_components']
        return len(host_components)    
    else:
        log.log(log.LOG_ERROR,'Unable to get the Datanode count: '+r.content)
        sys.exit(1)

def removeComponent(host,component,configdata):
     clustername = configdata['hdp']['clustername']
     hostname = host['name']
     log.log(log.LOG_INFO,'Removing {0} on {1}'.format(component,hostname))
     path = 'clusters/{0}/hosts/{1}/host_components/{2}'.format(clustername,hostname,component)
     r = delete(getambariUrl(configdata),getCredentials(configdata,'user'), getCredentials(configdata,'password'), path)
     response = json.dumps(r.content)
     if r.status_code in [200,202]:
         log.log(log.LOG_INFO,'Removed  {0} on {1}'.format(component,hostname))
     else:
         log.log(log.LOG_ERROR,'Unable to remove the {0} on {1} : {2}'.format(component,hostname,r.content))
         sys.exit(1)

def stopComponent(host,component,configdata):
     clustername = configdata['hdp']['clustername']
     hostname = host['name']
     log.log(log.LOG_INFO,'Stopping {0} on {1}'.format(component,hostname))
     requestbody = json.dumps({"RequestInfo":{"context":"Stop Component"},"Body":{"HostRoles":{"state":"INSTALLED"}}})
     path = 'clusters/{0}/hosts/{1}/host_components/{2}'.format(clustername,hostname,component)
     r = put(getambariUrl(configdata),getCredentials(configdata,'user'), getCredentials(configdata,'password'), path, requestbody)
     response = json.dumps(r.content)
     if r.status_code in [200,202]:
         request_id = json.loads(r.content)['Requests']['id']
         log.log(log.LOG_INFO,'Waiting for stop response of {0} on {1}'.format(component,hostname))
         status = wait_for_request_complete(getambariUrl(configdata),getCredentials(configdata,'user'),getCredentials(configdata,'password'),configdata.get('hdp').get('clustername'), request_id, 10)
     else:
     
         log.log(log.LOG_ERROR,'Unable to stop {0} on {1} : {2}'.format(component,hostname,r.content))
         sys.exit(1)


def clearHost(host,configdata):
     clustername = configdata['hdp']['clustername']
     hostname = host['name']
     log.log(log.LOG_INFO,'Removing {0} from {1}'.format(hostname,clustername))
     path = 'clusters/{0}/hosts/{1}'.format(clustername,hostname)
     r = delete(getambariUrl(configdata),getCredentials(configdata,'user'), getCredentials(configdata,'password'), path)
     if r.status_code  in [200,202] :
         log.log(log.LOG_WARN,'Removed  {0} from {1}'.format(hostname,clustername))
     else:
         log.log(log.LOG_ERROR,'Unable to Remove  {0} from {1} : {2}'.format(hostname,clustername,r.content))
         sys.exit(1)


def getComponentState(host,component,config):
    clustername = config['hdp']['clustername']
    hostname = host['name']
    path = 'clusters/{0}/hosts/{1}/host_components/{2}'.format(clustername,hostname,component)

    r = get(getambariUrl(config),getCredentials(config,'user'), getCredentials(config,'password'), path)

    if r.status_code == 200:
        return json.loads(r.content)['HostRoles']['state']
    else:
        log.log(log.LOG_ERROR,'Unable to get the state of component {0} on {1} :{2} '.format(component,hostname,json.loads(r.content)['message']))
        sys.exit(1)


def decomissionComponentOnHost(host,component,configdata):
     
     clustername = configdata['hdp']['clustername']
     hostname = host['name']
     log.log(log.LOG_INFO,'Decomissioning {0} on {1}'.format(component,hostname))
     requestbody = ''
     if component == 'DATANODE': 
        requestbody =json.dumps({ "RequestInfo": { "context": "Decomission DataNode", "command": "DECOMMISSION", "parameters": { "slave_type": "DATANODE", "excluded_hosts": "{0}".format(hostname) }, "operation_level": { "level": "HOST_COMPONENT", "cluster_name": "{0}".format(clustername) } }, "Requests/resource_filters": [ { "service_name": "HDFS", "component_name": "NAMENODE" } ] })
     elif component == 'NODEMANAGER': 
        requestbody =json.dumps({ "RequestInfo": { "context": "Decomission Nodemanager", "command": "DECOMMISSION", "parameters": { "slave_type": "NODEMANAGER", "excluded_hosts": "{0}".format(hostname) }, "operation_level": { "level": "HOST_COMPONENT", "cluster_name": "{0}".format(clustername) } }, "Requests/resource_filters": [ { "service_name": "YARN", "component_name": "RESOURCEMANAGER" } ] })
     path = 'clusters/{0}/requests'.format(clustername)
     r = post(getambariUrl(configdata),getCredentials(configdata,'user'), getCredentials(configdata,'password'), path, requestbody)  
     response = json.dumps(r.content)
     if r.status_code in [202,200]:
         request_id = json.loads(r.content)['Requests']['id']
         log.log(log.LOG_INFO,'Waiting for decomission response of {0} on {1}'.format(component,hostname))
         status = wait_for_request_complete(getambariUrl(configdata),getCredentials(configdata,'user'),getCredentials(configdata,'password'),configdata.get('hdp').get('clustername'), request_id, 10)
         if status == 'COMPLETED':
               log.log(log.LOG_INFO,'Decomissioned {0} on {1}'.format(component,hostname))
         else:
              log.log(log.LOG_INFO,'Failed to decomission {0} on {1} : {2}'.format(component,hostname,status))
              sys.exit(1)
     else:
         log.log(log.LOG_ERROR,'Unable to decomission the {0} on {1} : {2}'.format(component,hostname,r.content))
         sys.exit(1)
  
def removeHost(host,configdata):

    components = gethostcomponents(host['name'],configdata)
    
    for component in components:
        state = getComponentState(host,component,configdata) 
        if state == 'STARTED':
           if component in  ['DATANODE','NODEMANAGER']:
                 decomissionComponentOnHost(host,component,configdata)
        stopComponent(host,component,configdata) 
	removeComponent(host,component,configdata)       
    clearHost(host,configdata)         

def addHosts(configdata):
	    
    hdpAddHosts  = configdata.get('hdp').get('add',None)
	   
    if hdpAddHosts is not None:
         hdpHosts     = hdpAddHosts.get('hosts',[])
	 hostgroup    = hdpAddHosts.get('hostgroup')
	 for host in hdpHosts:
	     r = addhost2group(host.get('name'),hostgroup,configdata) 
	     response = json.dumps(r.content)
            
	     if r.status_code == 202:
		  request_id = json.loads(r.content)['Requests']['id']
		  log.log(log.LOG_INFO,'Wating for ambari to add {0} to {1}'.format(host['name'], hostgroup))
           	  status = wait_for_request_complete(getambariUrl(configdata),getCredentials(configdata,'user'),getCredentials(configdata,'password'),configdata.get('hdp').get('clustername'), request_id, 10)
                  if r.status_code == 403:
                   log.log(log.LOG_ERROR,'ambari: '+json.loads(r.content)['message'])
                   sys.exit(1)
                  else:
                     log.log(log.LOG_INFO,'{0} added to {1}'.format(host['name'],hostgroup))
             else:
                log.log(log.LOG_ERROR,'Unable to add {0} to {1} : {2}'.format(host['name'],hostgroup,r.content))  
def gethostcomponents(host,configdata):
    path = 'clusters/'+configdata['hdp']['clustername']+'/hosts/'+host
    r = get(getambariUrl(configdata),getCredentials(configdata,'user'), getCredentials(configdata,'password'), path)
    
    hostcomponents = ['DATANODE','NODEMANAGER','METRICS_MONITOR']
    components = []
    if r.status_code == 200:
        host_components = json.loads(r.content)['host_components']
        for host_component in host_components:
            component_name =  host_component['HostRoles']['component_name']
            if component_name in hostcomponents:
                components.append(component_name)
            else:
                log.log(log.LOG_WARN,'Found unexpected component {0} on host {1}'.format(component_name,host))
                sys.exit(1)
        return components
    else:
       log.log(log.LOG_ERROR,'ambari: '+str(json.loads(r.content)))
       log.log(log.LOG_ERROR,'unable to get the components info of the host {0}'.format(host))
       sys.exit(1)
    

def removeHosts(configdata):
    datanodecount =  getDataNodeCount(configdata)
    hdp = configdata['hdp']
    deletehosts = hdp.get('remove',dict()).get('hosts',[])
    log.log(log.LOG_INFO,'Removing hosts')      
    if (datanodecount - len(deletehosts)) > 0:
       for host in deletehosts:
            removeHost(host,configdata)
    else:
     log.log(log.LOG_ERROR,'Cluster has only one data node, cannot procced')
     log.log(log.LOG_ERROR,'Current datanode count {0} and expect to delete {1}'.format(datanodecount,1))
   

def getCredentials(configdata,key):
    return configdata['ambari'][key]
   

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
            config['ambari']['user'] = sys.argv[2]
            config['ambari']['password'] = sys.argv[3]
            addHosts(config)   
            removeHosts(config)     
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

