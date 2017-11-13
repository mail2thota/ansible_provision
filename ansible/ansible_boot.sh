#!/bin/bash

set -e

#confgure the ansible callback plugin for foreman

# execution of playbooks
echo "execution of playbook"
rm -rf executed_playbooks
mkdir executed_playbooks
cp -r  ambari-hdp executed_playbooks/

cd executed_playbooks/ambari-hdp
ansible-playbook playbooks/pre-config.yml
ansible-playbook playbooks/ambari_install.yml 

