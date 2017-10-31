#!/bin/bash
cd /home/hdfs/
mkdir -p /home/hdfs/spark/output
hadoop fs -rm -r -f /spark
hdfs dfs -mkdir -p /spark/input
hdfs dfs -mkdir -p /spark/output
hdfs dfs -put /home/hdfs/spark/inputfile.txt /spark/input

spark-submit --master yarn --deploy-mode client --executor-memory 1g \
--name wordcount --conf "spark.app.id=wordcount" /home/hdfs/spark/spark_test.py hdfs://agent1-ambariagent.example.com:8020/spark/input/inputfile.txt 2
