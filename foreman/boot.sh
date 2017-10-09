#!/bin/bash
#initialization foreman script
#author:Heri Sutrisno
#email:harry.sutrisno@baesystems.com
REPODIR=`dirname $0`
set -e
source ${REPODIR}/hammer_cfg.sh


if [[ $EUID -ne 0 ]]; then
  echo "You must be a root user" 2>&1
  exit 1
fi
echo "install foreman"

${REPODIR}/install.sh
${REPODIR}/dns_script/dns_boot.sh
${REPODIR}/foreman_proxy.sh
${REPODIR}/hammer.sh
${REPODIR}/foreman_provisioning.sh
cd ../ansible
./ansible_boot.sh
exit 0
