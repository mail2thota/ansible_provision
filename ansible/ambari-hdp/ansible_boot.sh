#!/bin/bash

set -e

echo "execution of playbook"
ansible-playbook playbooks/pre-config.yml
ansible-playbook playbooks/ambari_install.yml 

