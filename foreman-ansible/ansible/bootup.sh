#!/bin/bash

thisdir=`dirname $0`
source ${thisdir}/ansible_epel

#url for installation of ansible at the first time
url_repo=http://10.129.6.237





#--------------------------------------------------------------------
if [[ $EUID -ne 0 ]]; then
  echo "You must be a root user" 2>&1
  exit 1
fi
echo "install foreman"

setBaseRepo
setEpelRepo
yum clean all
yum install ansible -y
ansible-playbook foreman.yml -i ${thisdir}/inventory -u root
