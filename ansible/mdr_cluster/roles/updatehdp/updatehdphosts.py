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
    try:
      r = requests.get(ambari_url + path, auth=(user, password))
      return r
    except Exception as e:
         log.log(log.LOG_ERROR,'Not able to connect to ambari server@{0} Reason : {1}'.format(ambari_url,e))
         sys.exit(1)


def getambariUrl(configData):

    return "http://"+str(configData['ambari']['host'])+":"+str(configData["ambari"]["port"])+"/api/v1/"

def getClusterHosts(configdata):


   hdphosts = []
   path = 'clusters/'+configdata['hdp']['clustername']+'/hosts'
   r = get(getambariUrl(configdata),configdata['ambari']['user'], configdata['ambari']['password'], path)
   if r.status_code == 200 :
 
       hosts = json.loads(r.content)['items']
       
       for host in hosts:
                hdphosts.append(host['Hosts']['host_name'])
     
   else:
     log.log(log.LOG_ERROR,'Unable to retrive hosts from ambari: {0}'.format(r.content))
     sys.exit(1)

   with open('hosts','w') as hostFile:
       hostFile.write("\n[hdp]")
       #node_user = configdata['common'].get('node_user','root')
       #node_pass = configdata['common'].get('node_pass')
       for host in hdphosts:
                hostFile.write("\n"'{0}'.format(host))
  

def generateHostFile(configData):

   hostsipmap = dict({})

   hosts = configData['hdp']
   if len(hosts['add']['hosts']) == 0:
        log.log(log.LOG_WARN,'add hosts are empty')
        return
   with open('hosts','a') as hostFile:
	       hostFile.write("\n[hdp_add]")
	       #node_user = configData['common'].get('node_user','root')
	       #node_pass = configData['common'].get('node_pass')
	       for host in hosts['add']['hosts']:
		    hostFile.write("\n"'{0}'.format(host['name']))
   	            if 'ip' in  host:
        	           hostsipmap[host['ip']] = host['name']  
               hostFile.write("\n[ambari]")
               hostFile.write("\n"'{0}'.format(configData['ambari']['host']))

        
   with open('add_hosts','w') as hostFile:
       for host in hostsipmap:
                hostFile.write('{0} {1}\n'.format(host,hostsipmap[host]))

def generateAllFile(config):
    with open('all', 'w') as allFile:
        allFile.write("\n\n\n\n#Generated by script ")
        for service in config:
            allFile.write("\n\n#Service :" + service)
            for property in config[service]:
                if property == 'host':
                      hostgroup = []
                      hostgroup.append(dict({"name": config[service][property]}))               
                      allFile.write("\n" + service + "_hosts: "+ str(hostgroup))
                else:
                    allFile.write("\n" + service + "_" + property + ": " + str(config[service][property]))
    allFile.close()
  

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
            generateAllFile(config)   
            getClusterHosts(config)      
            generateHostFile(config) 
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

