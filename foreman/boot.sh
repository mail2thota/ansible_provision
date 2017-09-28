#initialization foreman script
#author:Heri Sutrisno
#!/bin/bash
REPODIR=`dirname $0`
source ${REPODIR}/hammer_cfg.sh


if [[ $EUID -ne 0 ]]; then
  echo "You must be a root user" 2>&1
  exit 1
fi
echo "install foreman"

${REPODIR}/install.sh
${REPODIR}/foreman_proxy.sh
${REPODIR}/hammer.sh
${REPODIR}/foreman_provisioning.sh
${REPODIR}/ansible_boot.sh
exit 0
