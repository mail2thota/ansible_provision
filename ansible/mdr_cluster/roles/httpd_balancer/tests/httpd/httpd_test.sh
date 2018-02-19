#!/bin/bash
actual_test_data="testing httpd"
echo "${actual_test_data}" > /var/www/html/index.html
retrieved_test_var=$(curl -L "localhost:80")
if [ "$retrieved_test_var" = "$actual_test_data" ]
then
 echo "httpd test is Successful"
else
 echo "httpd test is Failed"
fi

