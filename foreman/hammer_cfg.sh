#config file for creating foreman resources
#author:Heri Sutrisno
#email:herygranding@gmail.com

username=admin
password=as123
architecture="x86_64"
domain=example.com
url_repo=http://10.129.6.237
dns_id="foreman.example.com"

medium_name="CentOSDemo7"
image_path="http://10.129.6.237/repos/CentOS_7_x86_64"

os_name="CentOSDemo7"
os_majorversion=7
os_minorversion=2
os_family="Redhat"

template_default="Kickstart default"
template_finish="Kickstart default finish"
template_ipxe="Kickstart default iPXE"
template_pxelinux="Kickstart default PXELinux"
template_userdata="Kickstart default user data"

subnet_name="subnetDemo"
subnet_network="10.11.12.0"
subnet_mask="255.255.255.0"
subnet_gateway="10.11.12.1"
subnetip_start=10.11.12.1
subnetip_end=10.11.12.24
dhcp_interface="enp0s3"

environment="development"
host_groupname="groupA.example.com"
node_pass="as12345678"


number_of_master=1
master1=080027DC7005
master1ip=10.11.12.10

number_of_agent=1
agent1=08002704E9E5
agent1ip=10.11.12.11
