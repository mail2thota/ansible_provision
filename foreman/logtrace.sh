#!/bin/bash
#manage logging
#author:Heri Sutrisno
#email:harry.sutrisno@baesystems.com
set -e
thisdir=`dirname $0`
provision_log="${thisdir}/log/list_node"
log_dir="${thisdir}/log"
node_log="${thisdir}/log/foreman.log"

setLogFile(){

    if [ ! -d "$log_dir" ];
    then
        mkdir -p $log_dir
    fi

    if [ ! -e $node_log ];
    then
        echo "create $node_log"
        echo > $node_log
    fi

    if [ ! -e $provision_log ];
    then
        echo "create $provision_log"
        echo > $provision_log
        return
    fi
    
    echo "" > $provision_log
    echo "" > $node_log
}


