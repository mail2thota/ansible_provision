#!/bin/bash
service_name=$1
version=$2
url=$3
cluster_name=$7
report_path=/tmp/"${cluster_name}"_report_json
actual_path=$( echo $4 | cut -d':' -f2 )
trim_path=$( echo $actual_path | xargs )
path=$( echo $trim_path | tr "%" " " )
template="\"host\" : \""$5\"",\"status\" : \""$6\"""
if [ ! -d "$report_path" ]; then
  mkdir "${report_path}"
fi
if [ ! -f "${report_path}"/"${service_name}${version}".json ]; then
echo -e  "{\"service\":\""$service_name"\",\"version\":\""$version"\",\"url\":\""$url"\",\"path\":\""$path"\", \"properties\": [ { $template }]}" > "${report_path}"/"${service_name}${version}".json
else
sed -i "s%}]}% },{ $template }]}%g" "${report_path}"/"${service_name}${version}".json
fi






