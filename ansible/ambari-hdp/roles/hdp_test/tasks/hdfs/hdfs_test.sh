#!/bin/bash

echo "test test" > wordcountfile

sudo -u hdfs hdfs dfs -chmod 777 /

hdfs dfs -mkdir /wordcount



hdfs dfs -mkdir /wordcount/input



hdfs dfs -mkdir /wordcount/output



hdfs dfs -put wordcountfile /wordcount/input



hdfs hadoop jar /usr/hdp/2.6.2.0-205/hadoop-mapreduce/hadoop-mapreduce-examples.jar wordcount /wordcount/input/wordcountfile /wordcount/output/wordcountfile-output



sudo atd



hdfs hadoop dfs -cat /wordcount/output/wordcountfile-output/part-r-00000



hdfs dfs -getmerge /wordcount/output/wordcountfile-output /tmp/wordcountfile-output



head /tmp/wordcountfile-output 



echo "$(cat /tmp/wordcountfile-output | tr -d " \t\n\r")" > /tmp/wordcountfile-output



wordcountfile_output=$(awk '$1=$1' ORS='\\n' /tmp/wordcountfile-output)



if [[ $wordcountfile_output == *"2"* ]];then

	echo "HDFS test is Successful"

else

	echo "HDFS test is Failed"

fi
