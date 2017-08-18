INIT_SERVER_NAME_GROUPS=1-ambariservers-ambariagents,2-ambariagents
init_server_list_count=1
for init_server_name_groups in $(echo $INIT_SERVER_NAME_GROUPS | sed "s/,/ /g")
do
	init_server_count="$(cut -d '-' -f 1 <<< "${init_server_name_groups}")"
	init_server_group_name="$(cut -d '-' -f 2- <<< "${init_server_name_groups}")"
	while [ $init_server_count -gt 0 ]
		do
			init_server_list[init_server_list_count++]="${init_server_group_name}"
			((init_server_count--))
		done
done


get_host_name(){
 if [ $init_server_list_count -gt 1 ];then
	init_server_list_count=`expr $init_server_list_count - 1`
	echo  -${init_server_list[$init_server_list_count]}
 fi
}
#######so the hostname should be set as ${MACaddress}-ambariagents
get_host_name
#o/p -ambariagents
get_host_name
#o/p -ambariagents
#######

#######so the hostname should be set as ${MACaddress}-ambariservers-ambariagents
get_host_name
#o/p -ambariservers-ambariagents
#######

#######so the hostname should be set as ${MACaddress}
get_host_name
#o/p **nothing**
get_host_name
#o/p **nothing**
#######