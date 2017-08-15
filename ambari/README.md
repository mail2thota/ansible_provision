

##Manullay installing Ambari and Launching HDP cluster
    
  The Ambari Cluster launched using the ansible playbooks available in the ambari folder and before executing
  
#####Steps need to launch the ambari cluster 
    
######Step 1 - Configuring  ansible hosts 
   Preconfigure all the hosts in the  /etc/ansible/hosts into two groups
  
   1. ambariservers :  List of hosts on which the ambari server/master will be installed 
   2. ambariagents  :  List of hosts on which the ambari agents needs to be installed 
  
   From the above two groups hosts list ansible playbooks determine the list of ambari master hosts and slaves 
   
######Step 2 - Configuring SSH authentication optional

   Configure the password less authentication form the machine to all hosts(optional) using the below command
  
         ssh-copy-id root@<hostname>
    
  
######Step 3 - Installing,Setup and Starting Ambari

 
  Navigate to ambari folder and run the below command to execute the playbooks sequentially
  
  Installing Ambari Master
  
  if password less ssh authentication is configured
   
           ansible-playbook playbooks/conf/ambari/ambari_server.yml
  
  if password less ssh autnetication is not configured
      
           ansible-playbook playbooks/conf/ambari/ambari_server.yml -k -s
           
  without ssh authetication prompts the credentials of the hosts during the playbook execution
  
  Starting Ambari Master
  
  if password less ssh authentication is configured
      
    ansible-playbook playbooks/operation/ambari/setup.yml
     
  if passwordless ssh autnetication is not configured
         
    ansible-playbook playbooks/operation/ambari/setup.yml -k -s
              
   without ssh authetication prompts the credentials of the hosts during the playbook execution 
   
   with the above two steps we can access the ambari interface on the 8080 port(https://ambarihost.com:8080) of the ambari master host and the 
   credentils are admin/admin    
     
   Installing and Starting Agents
   
   if password less ssh authentication is configured
         
    ansible-playbook playbooks/conf/ambari/ambari_agent.yml
        
   if passwordless ssh autnetication is not configured
            
    ansible-playbook playbooks/operation/ambari/ambari_agent.yml -k -s
                 
   without ssh authetication prompts the credentials of the hosts during the playbook execution
   
   with the above scripts it will install the ambari agents in all the hosts and up running 
   
######Step 3 - Launching HDP Cluster using blue prints
   
  Navigate to the hdp folder
   
  Submiting the blueprints to ambari cluster 
         
     
  	curl -v -H "X-Requested-By: ambari" -X POST -u "${AMBARI_USER_NAME}":"${AMBARI_PASSWORD}" -d @hdp2.4-blueprint-multinode.json --noproxy "${ambari_server_domain}" http://"${ambari_server_domain}":8080/api/v1/blueprints/multi-node-hdfs


  Launching the cluster
   
     curl -v -H "X-Requested-By: ambari" -X POST -u "${AMBARI_USER_NAME}":"${AMBARI_PASSWORD}" -d @hdp2.4-multinode-hostconfig.json --noproxy "${ambari_server_domain}" http://"${ambari_server_domain}":8080/api/v1/clusters/multi-node-hdfs

  
  Now the cluster initializing will show in the ambari interface (https://ambarihost.com:8080) at and can be tracked and will take some time to cluster ready to use
   
   
   
   