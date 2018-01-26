#!/bin/bash
kibana_status=$(curl -H "Accept: application/json" http://localhost:5601/api/status -s | grep -i red | wc -l)
if [ "${kibana_status}" = '0' ]
then
 echo "kibana test is Successful"
else
 echo "kibana test is Failed"
fi

