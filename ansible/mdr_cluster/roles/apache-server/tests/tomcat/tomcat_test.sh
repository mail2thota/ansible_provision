actual_test_var=$(grep -Po "(?<=^helloworld.title).*" /var/lib/tomcat/webapps/examples/WEB-INF/classes/LocalStrings.properties)
curl -L "localhost:8080/examples/servlets/servlet/HelloWorldExample" > tomcat_test
retrieved_test_var=$(sed -n 's/<title>\(.*\)<\/title>/\1/Ip' tomcat_test)
if [ "$retrieved_test_var" = "${actual_test_var//=}" ]
then
 echo "tomcat test is Successful"
else
 echo "tomcat test is Failed"
fi

