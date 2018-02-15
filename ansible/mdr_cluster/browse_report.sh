#!/bin/bash
report_host=$1
cluser_id=$( echo $2 | tr "%" " " )
report_url="http://${report_host}?cluster_name=${cluser_id}"
is_shell_login=$(shopt -q login_shell && echo 'yes' || echo 'no')
if [ "$DESKTOP_SESSION" = "gnome-classic" -a "$is_shell_login" == "no" ]
 then
   xdg-open "${report_url}"
  else
   echo "NOTE:Web browser not supported in this machine.Please check overall status report through url ${report_url} in the machine that supports web browser."
fi






