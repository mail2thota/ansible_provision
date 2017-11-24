#!/bin/bash
rm -rf /etc/yum.repos.d/* 
if [ -d /tmp/yum.repos.d.tmp ]; then
  mv /tmp/yum.repos.d.tmp/* /etc/yum.repos.d
  rm -rf /tmp/yum.repos.d.tmp
fi

