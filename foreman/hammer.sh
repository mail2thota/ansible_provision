#!/bin/bash
#author: Heri Sutrisno

REPODIR=`dirname $0`
source ${REPODIR}/hammer_cfg.sh

# Create Architecture (if not alreay there)
if [ -z "$(hammer -u $USERNAME -p $PASSWORD architecture list | /usr/bin/grep "$ARCHITECTURE")"  ]; then
	hammer -u $USERNAME -p $PASSWORD architecture create --name $ARCHITECTURE
else
	echo "Already created: Architecture"
fi

# Create Domain (if not alreay there)
if [ -z "$(hammer -u $USERNAME -p $PASSWORD domain list | /usr/bin/grep "$DOMAIN")"  ]; then
	hammer -u $USERNAME -p $PASSWORD domain create --name $DOMAIN --description "Base resolve domain"
else
	echo "Already created: Domain"
fi

# Update Domain with DNS-id
proxy_id=$(hammer -u $USERNAME -p $PASSWORD proxy list | /usr/bin/grep "$DNS_ID" | /usr/bin/cut -d' ' -f1)
hammer -u $USERNAME -p $PASSWORD domain update --name $DOMAIN --dns-id $proxy_id

# Create Installation Medium (if not alreay there)
if [ -z "$(hammer -u $USERNAME -p $PASSWORD medium list | /usr/bin/grep "$MEDIUM_NAME")"  ]; then
	hammer -u $USERNAME -p $PASSWORD medium create --name $MEDIUM_NAME --path $IMAGE_PATH --os-family $OS_FAMILY
else
	echo "Already created: Installation Medium"
fi

# Create OS (if not alreay there)
ptable_id=$(hammer -u $USERNAME -p $PASSWORD partition-table list | /usr/bin/grep "$TEMPLATE_DEFAULT" | /usr/bin/cut -d' ' -f1)
os_id=$(hammer -u $USERNAME -p $PASSWORD os list | /usr/bin/grep "$OS_NAME" | /usr/bin/cut -d' ' -f1)
architecture_id=$(hammer -u $USERNAME -p $PASSWORD architecture list | /usr/bin/grep "$ARCHITECTURE" | /usr/bin/cut -d' ' -f1)
medium_id=$(hammer -u $USERNAME -p $PASSWORD medium list | /usr/bin/grep "$MEDIUM_NAME" | /usr/bin/cut -d' ' -f1)
if [ -z $os_id  ]; then
	hammer -u $USERNAME -p $PASSWORD os create --name $OS_NAME --major $OS_MAJORVERSION --minor $OS_MINORVERSION --family $OS_FAMILY --release-name $MEDIUM_NAME
        os_id=$(hammer -u $USERNAME -p $PASSWORD os list | /usr/bin/grep "$OS_NAME" | /usr/bin/cut -d' ' -f1)
else
	echo "Already created: OS"
fi

# Update Provisioning Templates,update this
template_id_default=$(hammer -u $USERNAME -p $PASSWORD template list --search "$TEMPLATE_DEFAULT" | /usr/bin/grep "$TEMPLATE_DEFAULT" | /usr/bin/cut -c 1-25 | /usr/bin/grep "[[:space:]]$" | /usr/bin/cut -d' ' -f1)
template_id_finish=$(hammer -u $USERNAME -p $PASSWORD template list --search "$TEMPLATE_FINISH" | /usr/bin/grep "$TEMPLATE_FINISH" | /usr/bin/cut -d' ' -f1)
template_id_pxelinux=$(hammer -u $USERNAME -p $PASSWORD template list --search "$TEMPLATE_PXElINUX" | /usr/bin/grep "$TEMPLATE_PXElINUX" | /usr/bin/cut -d' ' -f1)
template_id_ipxelinux=$(hammer -u $USERNAME -p $PASSWORD template list --search "$TEMPLATE_iPXE" | /usr/bin/grep "$TEMPLATE_iPXE" | /usr/bin/cut -d' ' -f1)
template_id_userdata=$(hammer -u $USERNAME -p $PASSWORD template list --search "$TEMPLATE_USERDATA" | /usr/bin/grep "$TEMPLATE_USERDATA" | /usr/bin/cut -d' ' -f1)

hammer -u $USERNAME -p $PASSWORD template update --locked false --id $template_id_default
hammer -u $USERNAME -p $PASSWORD template update --locked false --id $template_id_finish
hammer -u $USERNAME -p $PASSWORD template update --locked false --id $template_id_pxelinux
hammer -u $USERNAME -p $PASSWORD template update --locked false --id $template_id_ipxelinux
hammer -u $USERNAME -p $PASSWORD template update --locked false --id $template_id_userdata

hammer -u $USERNAME -p $PASSWORD template update --id $template_id_default --operatingsystem-ids $os_id
hammer -u $USERNAME -p $PASSWORD template update --id $template_id_finish --operatingsystem-ids $os_id
hammer -u $USERNAME -p $PASSWORD template update --id $template_id_pxelinux --operatingsystem-ids $os_id
hammer -u $USERNAME -p $PASSWORD template update --id $template_id_ipxelinux --operatingsystem-ids $os_id
hammer -u $USERNAME -p $PASSWORD template update --id $template_id_userdata --operatingsystem-ids $os_id

# Update PXELinux global default
template_id_pxelinux_global_default=$(hammer -u $USERNAME -p $PASSWORD template list --search "PXELinux global default" | /usr/bin/grep "PXELinux global default" | /usr/bin/cut -d' ' -f1)
hammer -u $USERNAME -p $PASSWORD template update --locked false --id $template_id_pxelinux_global_default
hammer -u $USERNAME -p $PASSWORD template update --id $template_id_pxelinux_global_default --file $REPODIR/PXELinux_global_default

# Update Preseed Finish
#hammer template update --id $template_id_finish --file /home/server/git/foreman-poc/hammer/preseed_default_finish

# Update Puppet.conf
#template_id_puppetConf=$(hammer template list --search puppet.conf | /usr/bin/grep puppet.conf | /usr/bin/cut -d' ' -f1)
#hammer template update --id $template_id_puppetConf --file /home/server/git/foreman-poc/hammer/puppet.conf --type snippet

# Update Partition Table
#hammer partition-table update --id $ptable_id --file /home/server/git/foreman-poc/hammer/pTable
domain_id=$(hammer -u $USERNAME -p $PASSWORD domain list | /usr/bin/grep "$DOMAIN"  | /usr/bin/cut -d' ' -f1)

# Create Subnet (if not alreay there)
if [ -z "$(hammer -u $USERNAME -p $PASSWORD subnet list | /usr/bin/grep "$SUBNET_NAME")"  ]; then
	hammer -u $USERNAME -p $PASSWORD subnet create --name $SUBNET_NAME --network $SUBNET_NETWORK --mask $SUBNET_MASK --gateway $SUBNET_GATEWAY --domain-ids $domain_id --dhcp-id $proxy_id --tftp-id $proxy_id --dns-id $proxy_id
else
	echo "Already created: Subnet"
fi
# Create Environment (if not alreay there)
if [ -z "$(hammer -u $USERNAME -p $PASSWORD environment list | /usr/bin/grep "$ENVIRONMENT")"  ]; then
	hammer -u $USERNAME -p $PASSWORD environment create --name $ENVIRONMENT
else
	echo "Already created: Environment"
fi

#Create Hostgroup
environment_id=$(hammer -u $USERNAME -p $PASSWORD environment list --search $ENVIRONMENT | /usr/bin/grep "$ENVIRONMENT" | /usr/bin/cut -d' ' -f1)
subnet_id=$(hammer -u $USERNAME -p $PASSWORD subnet list --search $SUBNET_NAME |  /usr/bin/grep "$SUBNET_NAME" | /usr/bin/cut -d' ' -f1)
hammer -u $USERNAME -p $PASSWORD hostgroup create --name "$HOST_GROUPNAME" --environment-id "$environment_id" --operatingsystem-id "$os_id" --architecture-id "$architecture_id" --medium-id "$medium_id" --puppet-ca-proxy-id "$proxy_id" --subnet-id "$subnet_id" --domain-id "$domain_id" --puppet-proxy-id "$proxy_id"

hostgroup_id=$(hammer -u $USERNAME -p $PASSWORD hostgroup list --search "$HOST_GROUPNAME" | /usr/bin/grep "$HOST_GROUPNAME" | /usr/bin/cut -d' ' -f1)

hammer -u $USERNAME -p $PASSWORD hostgroup set-parameter --name 'drives' --value '/dev/sdb:/drv/drive01' --hostgroup-id $hostgroup_id

exit 0
