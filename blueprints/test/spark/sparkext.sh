mkdir -p /home/hdfs/output
hadoop fs -rm -r -f /spark
hdfs dfs -mkdir -p /spark/input
hdfs dfs -put ./inputfile.txt /spark/input

spark-submit --master yarn --deploy-mode client --executor-memory 1g \
--name wordcount --conf "spark.app.id=wordcount" ./spark_test.py hdfs://agent1-ambariagent.example.com:8020/spark/input/inputfile.txt 2
