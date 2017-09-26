# Setting HTTP server (NGINX)

  The HTTP server installation to setup local repository to provide centos iso, yum, epel, foreman, puppet, ansible, ambari, hdp, java and other required softwares and libraries 

## Steps to launch the HTTP Server (NGINX)

### Run http_repo_setup.sh script from nginx folder in mdr_platform_bare_metal
   Download mdr_platform_bare_metal repository and execute http_repo_setup.sh from nginx folder, NGINX server will be installed. 
   
   Options to execute.
   *  with out any argument
   *  with argument 'N'

   
### OPTION 1 - executing script with out any argument

   create repos folder under /usr/share/. Download and copy all required repositories to /usr/share/repos prior to executing the script.
   
   
  ```
    ./http_repo_setup.sh
  ```
#### Software listing:
Following are the required softwares and libraries in repository
| Software/library       |  URL to download           |
|:------------- |:-------------|
|Centos Base repo|rsync://mirror.cisp.com/CentOS/7/os/x86_64/|
|Centos Update repo|rsync://mirror.cisp.com/CentOS/7/updates/x86_64/|
|RH repo|rsync://mirror.cisp.com/CentOS/7/sclo/x86_64/rh/|
|SCLO repo|rsync://mirror.cisp.com/CentOS/7/sclo/x86_64/sclo/|
|EPEL 7 repo|rsync://mirrors.rit.edu/epel/7/x86_64/|
|Puppet Labs repo|rsync://yum.puppetlabs.com/el/7/PC1/x86_64/|
|Foreman repo|rsync://yum.theforeman.org/releases/1.15/el7/x86_64/|
|Foreman Plugins|rsync://yum.theforeman.org/plugins/1.15/el7/x86_64/|
|sclo repo|rsync://mirror.cisp.com/CentOS/7/sclo/x86_64|
|Centos 7 iso image|http://mirror.optus.net/centos/7/isos/x86_64/CentOS-7-x86_64-Everything-1611.iso|
|Ambari repo|http://public-repo-1.hortonworks.com/ambari/centos6/2.x/updates/2.5.0.3/ambari-2.5.0.3-centos6.tar.gz|
|HDP repo|http://public-repo-1.hortonworks.com/HDP/centos7/2.x/updates/2.6.2.0/HDP-2.6.2.0-centos7-rpm.tar.gz|
|RPM-GPG-KEY-CentOS-7 key|http://mirror.cisp.com/CentOS/7/os/x86_64/RPM-GPG-KEY-CentOS-7|
|RPM-GPG-KEY-CentOS-SIG-SCLo key|https://yum.stanford.edu/RPM-GPG-KEY-CentOS-SIG-SCLo|
|RPM-GPG-KEY-EPEL-7 key|http://mirrors.rit.edu/epel/RPM-GPG-KEY-EPEL-7|
|RPM-GPG-KEY-foreman key|http://yum.theforeman.org/releases/1.15/RPM-GPG-KEY-foreman|
|RPM-GPG-KEY-puppet key|https://yum.puppetlabs.com/RPM-GPG-KEY-puppet|
|RPM-GPG-KEY-puppetlabs key|https://yum.puppetlabs.com/RPM-GPG-KEY-puppetlabs|

##### Note: rsync links required to install rsync package on bootstrap machine and all tars must be unzipped.

### OPTION 2 - executing script with argument 'N'
Installs NGINX server and downloads all required repositories from internet.

##### Note: This required internet connection
  ```
    ./http_repo_setup.sh N
  ```
  
## Licence:
mdr_platform_bare_metal  - Copyright (c) 2017 BAE Systems Applied Intelligence.
