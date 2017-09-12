#!/bin/bash
REPODIR=`dirname $0`
source ${REPODIR}/hammer_cfg.sh


${REPODIR}/foreman_proxy.sh
${REPODIR}/hammer.sh
${REPODIR}/foreman_provisioning.sh
${REPODIR}/boot_ansible_hadoop.sh
exit 0
