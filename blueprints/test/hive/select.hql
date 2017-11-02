create schema ${hiveconf:DB_NAME};
show schemas;
use ${hiveconf:DB_NAME};
CREATE TABLE ${hiveconf:DB_NAME}.${hiveconf:TABLE_NAME} (ID INT, name STRING, dt STRING) ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n';
show tables;
LOAD DATA LOCAL INPATH './raw.txt' OVERWRITE INTO TABLE ${hiveconf:DB_NAME}.${hiveconf:TABLE_NAME};
select * from ${hiveconf:DB_NAME}.${hiveconf:TABLE_NAME};