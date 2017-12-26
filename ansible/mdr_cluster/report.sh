#!/bin/bash
service_name=$1
version=$2
url=$3
actual_path=$( echo $4 | cut -d':' -f2 )
trim_path=$( echo $actual_path | xargs )
path=$( echo $trim_path | tr "%" " " )
template="\"host\" : \""$5\"",\"status\" : \""$6\"""
if [ ! -f /tmp/report_json/"${service_name}".json ]; then
echo -e  "{\"service\":\""$service_name"\",\"version\":\""$version"\",\"url\":\""$url"\",\"path\":\""$path"\", \"properties\": [ { $template }]}" > /tmp/report_json/"${service_name}".json
else
sed -i "s%}]}% },{ $template }]}%g" /tmp/report_json/"${service_name}".json
fi






