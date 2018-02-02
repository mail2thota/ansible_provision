#!/bin/bash
cluster_name=$1
reports=/tmp/"${cluster_name}"_report_json/*.json
count=0
overall_report=/tmp/"${cluster_name}"_overall_report.json
> "${overall_report}"
echo "{"  >> "${overall_report}"
echo "\"reports\":["  >> "${overall_report}"
for report in $reports
do
  if [ "$count" -gt "0" ]; then
   echo "," >> "${overall_report}"
echo "$count" 
  fi
  cat $report >> "${overall_report}"
  count=$((count+1))
done
echo "]}" >> "${overall_report}"






