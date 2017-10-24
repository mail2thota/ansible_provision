#!/bin/bash

echo "test test" > wordcountfile

sudo -u hdfs hdfs dfs -chmod 777 /

/usr/hdp/2.6.2.0-205/hadoop/bin/hdfs dfs -mkdir /wordcount



/usr/hdp/2.6.2.0-205/hadoop/bin/hdfs dfs -mkdir /wordcount/input



/usr/hdp/2.6.2.0-205/hadoop/bin/hdfs dfs -mkdir /wordcount/output



/usr/hdp/2.6.2.0-205/hadoop/bin/hdfs dfs -put wordcountfile /wordcount/input



su hdfs /usr/hdp/2.6.2.0-205/hadoop/bin/hadoop jar /usr/hdp/2.6.2.0-205/hadoop-mapreduce/hadoop-mapreduce-examples.jar wordcount /wordcount/input/wordcountfile /wordcount/output/wordcountfile-output



sudo atd



su hdfs /usr/hdp/2.6.2.0-205/hadoop/bin/hadoop dfs -cat /wordcount/output/wordcountfile-output/part-r-00000



/usr/hdp/2.6.2.0-205/hadoop/bin/hdfs dfs -getmerge /wordcount/output/wordcountfile-output /tmp/wordcountfile-output



head /tmp/wordcountfile-output 



echo "$(cat /tmp/wordcountfile-output | tr -d " \t\n\r")" > /tmp/wordcountfile-output



wordcountfile_output=$(awk '$1=$1' ORS='\\n' /tmp/wordcountfile-output)



if [[ $wordcountfile_output == *"2"* ]];then

	echo "HDFS test is Successful"

else

	echo "HDFS test is Failed"

fi
