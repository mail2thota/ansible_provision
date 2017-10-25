#!/bin/bash

cd /home/hdfs

yarn jar /usr/hdp/2.6.2.0-205/hadoop-mapreduce/hadoop-mapreduce-examples.jar pi 16 1000 > yarn_test


yarn_output=$(awk '$1=$1' ORS='\\n' /home/hdfs/yarn_test)



if [[ $yarn_output == *"Estimated value of Pi is 3.14250000000000000000"* ]];then

	echo "Yarn test is Successful"

else

	echo "Yarn test is Failed"

fi