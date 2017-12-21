#!/bin/bash
reports=/tmp/report_json/*.json
count=0
overall_report=/tmp/overall_report.json
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
rm -rf /tmp/report_json





