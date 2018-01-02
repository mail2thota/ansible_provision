#!/bin/bash
httpd_test_web="overallreport.com"
httpd_test_data="testing httpd"
mkdir -p /var/www/"${httpd_test_web}"/public_html
chown -R $USER:$USER /var/www/"${httpd_test_web}"/public_html
chmod -R 755 /var/www
echo "${httpd_test_data}" >/var/www/"${httpd_test_web}"/public_html/index.html
mkdir /etc/httpd/sites-available
mkdir /etc/httpd/sites-enabled
echo "IncludeOptional sites-enabled/*.conf" >> /etc/httpd/conf/httpd.conf
echo -e  "<VirtualHost *:80> \n ServerName www.${httpd_test_web} \n ServerAlias ${httpd_test_web} \n DocumentRoot /var/www/${httpd_test_web}/public_html \n ErrorLog /var/www/${httpd_test_web}/error.log \n CustomLog /var/www/${httpd_test_web}/requests.log combined \n </VirtualHost>" > /etc/httpd/sites-available/"${httpd_test_web}".conf
ln -s /etc/httpd/sites-available/"${httpd_test_web}".conf /etc/httpd/sites-enabled/"${httpd_test_web}".conf
systemctl restart httpd
echo "$(hostname -i) ${httpd_test_web}" >> /etc/hosts
web_content=$(curl -L "${httpd_test_web}")
if [ "$web_content" = "${httpd_test_data}" ]
then
 echo "httpd test is Successful"
else
 echo "httpd test is Failed"
fi

