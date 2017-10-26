#!/bin/sh
FILE=./select.properties
db_name=$(grep -i 'databaseName' $FILE  | cut -f2 -d'=')
table_name=$(grep -i 'tableName' $FILE  | cut -f2 -d'=')
echo "connecting to database - " $db_name
echo  "using table - " $table_name
hive -hiveconf DB_NAME=$db_name -hiveconf TABLE_NAME=$table_name -f ./select.hql