#!/bin/bash

oozie_url=$1 
oozie_name_node=$2 
oozie_job_tracker=$3
echo "${oozie_url}"
sed -i "s%<OOZIE_NAME_NODE>%${oozie_name_node}%g" /home/hdfs/oozie/oozie-examples/job.properties
sed -i "s%<OOZIE_JOB_TRACKER>%${oozie_job_tracker}%g" /home/hdfs/oozie/oozie-examples/job.properties 
hdfs dfs -test -d /workflows
if [ $? == 0 ]; then
    hdfs dfs -rm -r -f /workflows
fi

hadoop fs -mkdir /workflows/
hadoop fs -put /home/hdfs/oozie/oozie-examples /workflows/oozie-examples
export OOZIE_URL="${oozie_url}"
oozie job -config /home/hdfs/oozie/oozie-examples/job.properties -run

