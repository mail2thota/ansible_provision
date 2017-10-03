#!/bin/bash
#automate foreman resources
#author:Heri Sutrisno
#email:herygranding@gmail.com
set -e
thisdir=`dirname $0`
source ${thisdir}/hammer_cfg.sh

setArchitecture(){
  
    # Create Architecture (if not alreay there)
    if [ -z "$(hammer -u $username -p $password architecture list | /usr/bin/grep -E "(^|\s)$architecture($|\s)")" ]; then
        hammer -u $username -p $password architecture create --name $architecture
        #log: create architecture name:$architecture
    else
       echo "set Architecture $architecture"
    fi
}

createDomain(){
    # Create Domain (if not alreay there)
    if [ -z "$(hammer -u $username -p $password domain list | /usr/bin/grep -E "(^|\s)$domain($|\s)")"  ]; then
        hammer -u $username -p $password domain create --name $domain --description $domain
    else
        echo "set Domain $domain"
    fi
}

createInstallMedium(){

    # Create Installation Medium (if not alreay there)
    if [ -z "$(hammer -u $username -p $password medium list | /usr/bin/grep -E "(^|\s)$medium_name($|\s)")"  ]; then
        hammer -u $username -p $password medium create --name $medium_name --path $image_path --os-family $os_family
    else
        echo "set Installation Medium $medium_name"
    fi
}

createOS(){

    # Create OS (if not already there)
    ptable_id=$(hammer -u $username -p $password partition-table list | /usr/bin/grep -E "(^|\s)$template_default($|\s)" | /usr/bin/cut -d' ' -f1)
    os_id=$(hammer -u $username -p $password os list | /usr/bin/grep -E "(^|\s)$os_name($|\s)" | /usr/bin/cut -d' ' -f1)
    architecture_id=$(hammer -u $username -p $password architecture list | /usr/bin/grep -E "(^|\s)$architecture($|\s)" | /usr/bin/cut -d' ' -f1)
    medium_id=$(hammer -u $username -p $password medium list | /usr/bin/grep -E "(^|\s)$medium_name($|\s)" | /usr/bin/cut -d' ' -f1)
    if [ -z $os_id  ]; 
    then
        hammer -u $username -p $password os create --name "$os_name" --major "$os_majorversion" --minor "$os_minorversion" --family "$os_family" --architecture-ids $architecture_id --partition-table-ids $ptable_id --medium-ids $medium_id --release-name "$medium_name"
        os_id=$(hammer -u $username -p $password os list | /usr/bin/grep -E "(^|\s)$os_name($|\s)" | /usr/bin/cut -d' ' -f1)
    else
        echo "set OS $os_name"
fi
}

updateTemplate(){

    # Update Provisioning Templates,update this
    template_id_default=$(hammer -u $username -p $password template list --search "$template_default" | /usr/bin/grep -E "(^|\s)$template_default($|\s)" | /usr/bin/cut -c 1-25 | /usr/bin/grep "[[:space:]]$" | /usr/bin/cut -d' ' -f1)
    template_id_finish=$(hammer -u $username -p $password template list --search "$template_finish" | /usr/bin/grep -E "(^|\s)$template_finish($|\s)" | /usr/bin/cut -d' ' -f1)
    template_id_pxelinux=$(hammer -u $username -p $password template list --search "$template_pxelinux" | /usr/bin/grep -E "(^|\s)$template_pxelinux($|\s)" | /usr/bin/cut -d' ' -f1)
    template_id_ipxelinux=$(hammer -u $username -p $password template list --search "$template_ipxe" | /usr/bin/grep -E "(^|\s)$template_ipxe($|\s)" | /usr/bin/cut -d' ' -f1)
    template_id_userdata=$(hammer -u $username -p $password template list --search "$template_userdata" | /usr/bin/grep -E "(^|\s)$template_userdata($|\s)" | /usr/bin/cut -d' ' -f1)

    echo "Unlock provisioning templates"
    hammer -u $username -p $password template update --locked false --id $template_id_default
    hammer -u $username -p $password template update --locked false --id $template_id_finish
    hammer -u $username -p $password template update --locked false --id $template_id_pxelinux
    hammer -u $username -p $password template update --locked false --id $template_id_ipxelinux
    hammer -u $username -p $password template update --locked false --id $template_id_userdata
    echo "Unlock provisioning templates end"

    #update Kickstarter_Default
    echo "Update Kickstart default"
    hammer -u $username -p $password template update --id $template_id_default --file $thisdir/Kickstart_default
    echo "Update Kickstart default end"

    echo "Update provisioning template"
    hammer -u $username -p $password template update --id $template_id_default --operatingsystem-ids $os_id
    hammer -u $username -p $password template update --id $template_id_finish --operatingsystem-ids $os_id
    hammer -u $username -p $password template update --id $template_id_pxelinux --operatingsystem-ids $os_id
    hammer -u $username -p $password template update --id $template_id_ipxelinux --operatingsystem-ids $os_id
    hammer -u $username -p $password template update --id $template_id_userdata --operatingsystem-ids $os_id
    echo "update provisioning template end"

    echo "Update media template Associate"
    hammer -u $username -p $password os set-default-template --id $os_id --config-template-id $template_id_default
    hammer -u $username -p $password os set-default-template --id $os_id --config-template-id $template_id_finish
    hammer -u $username -p $password os set-default-template --id $os_id --config-template-id $template_id_pxelinux
    hammer -u $username -p $password os set-default-template --id $os_id --config-template-id $template_id_ipxelinux
    hammer -u $username -p $password os set-default-template --id $os_id --config-template-id $template_id_userdata
    echo "end Associate"

}

createSubnet(){

    # Create Subnet (if not alreay there)
    if [ -z "$(hammer -u $username -p $password subnet list | /usr/bin/grep -E "(^|\s)$subnet_name($|\s)")"  ]; then
       env_label="production"
       if [ "${environment,,}" = "${env_label,,}" ];
       then
           hammer -u $username -p $password subnet create --name $subnet_name --network $subnet_network --mask $subnet_mask --gateway $subnet_gateway --ipam "DHCP" --from $subnetip_start --to $subnetip_end --domain-ids $domain_id --dhcp-id $proxy_id --tftp-id $proxy_id --boot-mode "DHCP"
          
       else
           hammer -u $username -p $password subnet create --name $subnet_name --network $subnet_network --mask $subnet_mask --gateway $subnet_gateway --ipam "DHCP" --from $subnetip_start --to $subnetip_end --domain-ids $domain_id --dhcp-id $proxy_id --tftp-id $proxy_id --boot-mode "Static"
       fi
    else
        echo "Already created: Subnet $subnet_name"
    fi
    echo "Create subnet end"
}

createEnvType(){

    echo "Create environment type"
    # Create Environment (if not alreay there)
    if [ -z "$(hammer -u $username -p $password environment list | /usr/bin/grep -E "(^|\s)$environment($|\s)")"  ]; then
        hammer -u $username -p $password environment create --name $environment
    else
        echo "Already created: Environment $environment"
    fi
    echo "Create environtment type end"

}

createParameters(){

    #global parameter
    echo "set global paramter"
    hammer -u $username -p $password global-parameter set --name disable-firewall --value true
    hammer -u $username -p $password global-parameter set --name package_upgrade --value false
    hammer -u $username -p $password global-parameter set --name enable-epel --value false
    hammer -u $username -p $password global-parameter set --name selinux-mode --value permissive
    hammer -u $username -p $password global-parameter set --name enable-puppetlabs-repo --value false
    hammer -u $username -p $password global-parameter set --name enable-puppetlabs-pc1-repo --value false
    echo "global parameter end"

}

createHostGroup(){
    
    echo "Create host group"
    #Create Hostgroup
    environment_id=$(hammer -u $username -p $password environment list --search $environment | /usr/bin/grep -E "(^|\s)$environment($|\s)" | /usr/bin/cut -d' ' -f1)
    subnet_id=$(hammer -u $username -p $password subnet list --search $subnet_name |  /usr/bin/grep -E "(^|\s)$subnet_name($|\s)" | /usr/bin/cut -d' ' -f1)
    if [ -z "$(hammer -u $username -p $password   hostgroup list | /usr/bin/grep -E "(^|\s)$host_groupname($|\s)")"  ]; then
        hammer -u $username -p $password hostgroup create --name "$host_groupname" --environment-id $environment_id --operatingsystem-id $os_id --architecture-id $architecture_id --medium-id $medium_id --partition-table-id $ptable_id --root-pass $node_pass --puppet-ca-proxy-id $proxy_id --subnet-id $subnet_id --domain-id $domain_id --puppet-proxy-id $proxy_id
    else
        echo "Already created: $host_groupname"
    fi
    echo "Create host group end"
}

generateTemplate(){
    
    subnet_id=$(hammer -u $username -p $password subnet list | /usr/bin/grep -E "(^|\s)$subnet_name($|\s)" | /usr/bin/cut -d' ' -f1)
    #proxy_id=$(hammer -u $username -p $password proxy list | /usr/bin/grep -E "(^|\s)$dns_id($|\s)" | /usr/bin/cut -d' ' -f1)
    #hammer -u $username -p $password subnet update --id $subnet_id --discovery-id $proxy_id
    hammer -u $username -p $password template build-pxe-default
    #HOST_GROUPID=$(hammer -u $username -p $password hostgroup list| /usr/bin/grep -E "(^|\s)$host_groupname($|\s)" | /usr/bin/cut -d' ' -f1)
}
setArchitecture
createDomain
proxy_id=$(hammer -u $username -p $password proxy list | /usr/bin/grep -E "(^|\s)$dns_id($|\s)" | /usr/bin/cut -d' ' -f1)
createInstallMedium
createOS
updateTemplate
domain_id=$(hammer -u $username -p $password domain list | /usr/bin/grep -E "(^|\s)$domain($|\s)" | /usr/bin/cut -d' ' -f1)
createSubnet
createEnvType
createParameters
createHostGroup
generateTemplate
exit 0
