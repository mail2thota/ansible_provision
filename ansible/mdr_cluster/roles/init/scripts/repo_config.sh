#!/bin/bash
rm -rf /tmp/yum.repos.d.tmp
shopt -s nullglob dotglob    
files=(/etc/yum.repos.d/*)
if [ ${#files[@]} -gt 0 ]
then 
	mkdir /tmp/yum.repos.d.tmp 
	mv /etc/yum.repos.d/* /tmp/yum.repos.d.tmp
fi




