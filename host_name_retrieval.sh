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


node_count=1
get_host_name(){
 if [ $init_server_list_count -gt 1 ];then
	init_server_list_count=`expr $init_server_list_count - 1`
	echo  node${node_count}-${init_server_list[$init_server_list_count]}
 else
	echo  node${node_count}
 fi
 node_count=`expr $node_count + 1`
}

get_host_name
#prints node1-abariagents
get_host_name
#prints node2-abariagents
get_host_name
#prints node3-abariservers-abariagents
get_host_name
#prints node4
get_host_name
#prints node5