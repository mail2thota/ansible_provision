#!/bin/bash
hadoop fs -rm -r /workflows/
hadoop fs -mkdir /workflows/
hadoop fs -put /home/hdfs/oozie/oozie-examples /workflows/oozie-examples
export OOZIE_URL=http://localhost:11000/oozie
oozie job -config /home/hdfs/oozie/oozie-examples/job.properties -run
