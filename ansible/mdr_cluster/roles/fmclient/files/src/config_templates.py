
import sys
def init(repo_url):
    global kickstarter_default
    global kickstarter_pxelinux
    kickstart_str='<%#\nkind: provision\nname: Kickstart default\noses:\n- CentOS\n- Fedora\n%>\n<%#\nThis template accepts the following parameters:\n- lang: string (default="en_US.UTF-8")\n- selinux-mode: string (default="enforcing")\n- keyboard: string (default="us")\n- time-zone: string (default="UTC")\n- http-proxy: string (default="")\n- http-proxy-port: string (default="")\n- force-puppet: boolean (default=false)\n- enable-epel: boolean (default=true)\n- enable-puppetlabs-repo: boolean (default=false)\n- enable-puppetlabs-pc1-repo: boolean (default=false)\n- salt_master: string (default=undef)\n- ntp-server: string (default="0.fedora.pool.ntp.org")\n- bootloader-append: string (default="nofb quiet splash=quiet")\n- disable-firewall: boolean (default=false)\n- package_upgrade: boolean (default=true)\n- disable-uek: boolean (default=false)\n%>\n<%\n  rhel_compatible = @host.operatingsystem.family == \'Redhat\' && @host.operatingsystem.name != \'Fedora\'\n  os_major = @host.operatingsystem.major.to_i\n  realm_compatible = (@host.operatingsystem.name == \'Fedora\' && os_major >= 20) || (rhel_compatible && os_major >= 7)\n  # safemode renderer does not support unary negation\n  pm_set = @host.puppetmaster.empty? ? false : true\n  proxy_uri = @host.params[\'http-proxy\'] ? "http://#{{@host.params[\'http-proxy\']}}:#{{@host.params[\'http-proxy-port\']}}" : nil\n  proxy_string = proxy_uri ? " --proxy=#{{proxy_uri}}" : \'\'\n  puppet_enabled = pm_set || @host.param_true?(\'force-puppet\')\n  salt_enabled = @host.params[\'salt_master\'] ? true : false\n  chef_enabled = @host.respond_to?(:chef_proxy) && @host.chef_proxy\n section_end = (rhel_compatible && os_major <= 5) ? \'\' : \'%end\'\n%>\ninstall\n<%= @mediapath %><%= proxy_string %>\nlang <%= @host.params[\'lang\'] || \'en_US.UTF-8\' %>\nselinux --<%= @host.params[\'selinux-mode\'] || @host.params[\'selinux\'] || \'enforcing\' %>\nkeyboard <%= @host.params[\'keyboard\'] || \'us\' %>\nskipx\n\n<% subnet = @host.subnet -%>\n<% if subnet.respond_to?(:dhcp_boot_mode?) -%>\n<% dhcp = subnet.dhcp_boot_mode? && !@static -%>\n<% else -%>\n<% dhcp = !@static -%>\n<% end -%>\nnetwork --bootproto <%= dhcp ? \'dhcp\' : "static --ip=#{{@host.ip}} --netmask=#{{subnet.mask}} --gateway=#{{subnet.gateway}} --nameserver=#{{[subnet.dns_primary, subnet.dns_secondary].select{{ |item| item.present? }}.join(\',\')}}" %> --hostname <%= @host %><%= os_major >= 6 ? " --device=#{{@host.mac}}" : \'\' -%>\n\nrootpw --iscrypted <%= root_pass %>\n<% if @host.param_true?(\'disable-firewall\') -%>\nfirewall --disable\n<% else -%>\nfirewall --<%= os_major >= 6 ? \'service=\' : \'\' %>ssh\n<% end -%>\nauthconfig --useshadow --passalgo=<%= @host.operatingsystem.password_hash || \'sha256\' %> --kickstart\ntimezone --utc <%= @host.params[\'time-zone\'] || \'UTC\' %>\n<% if rhel_compatible -%>\nservices --disabled gpm,sendmail,cups,pcmcia,isdn,rawdevices,hpoj,bluetooth,openibd,avahi-daemon,avahi-dnsconfd,hidd,hplip,pcscd\n<% end -%>\n\n<% if realm_compatible && @host.info[\'parameters\'][\'realm\'] && @host.realm && @host.realm.realm_type == \'Active Directory\' -%>\n# One-time password will be requested at install time. Otherwise, $HOST[OTP] is used as a placeholder value.\nrealm join --one-time-password=\'<%= @host.otp || "$HOST[OTP]" %>\' <%= @host.realm %>\n<% end -%>\n\n<% if @host.operatingsystem.name == \'Fedora\' -%>\nrepo --name=fedora-everything --mirrorlist=https://mirrors.fedoraproject.org/metalink?repo=fedora-<%= @host.operatingsystem.major %>&arch=<%= @host.architecture %><%= proxy_string %>\n<% end -%>\n\n<% if @host.operatingsystem.name == \'OracleLinux\' && os_major == 7 -%>\nrepo --name="Server-Mysql"\n<% end -%>\n\n<% if rhel_compatible -%>\nrepo --name=base --baseurl={0}/repos/centos/7/os/$basearch\nrepo --name=update --baseurl={0}/repos/centos/7/updates/$basearch\n<% end -%>\n\n<% if @host.operatingsystem.name == \'Fedora\' and os_major <= 16 -%>\n# Bootloader exception for Fedora 16:\nbootloader --append="<%= @host.params[\'bootloader-append\'] || \'nofb quiet splash=quiet\' %> <%=ks_console%>" <%= grub_pass %>\npart biosboot --fstype=biosboot --size=1\n<% else -%>\nbootloader --location=mbr --append="<%= @host.params[\'bootloader-append\'] || \'nofb quiet splash=quiet\' %>" <%= grub_pass %>\n<% if os_major == 5 -%>\nkey --skip\n<% end -%>\n<% end -%>\n\n<% if @dynamic -%>\n%include /tmp/diskpart.cfg\n<% else -%>\n<%= @host.diskLayout %>\n<% end -%>\n\ntext\n<% if @host.respond_to?(:bootdisk_build?) && @host.bootdisk_build? %>\nreboot --eject\n<% else -%>\nreboot\n<% end -%>\n\n%packages\nyum\ndhclient\nntp\nwget\nNetworkManager-dispatcher-routing-rules\n@Core\n<% if os_major >= 6 -%>\nredhat-lsb-core\n<% end -%>\n<% if salt_enabled %>\nsalt-minion\n<% end -%>\n<%= section_end -%>\n\n<% if @dynamic -%>\n%pre\n<%= @host.diskLayout %>\n<%= section_end -%>\n<% end -%>\n\n%post --nochroot\nexec < /dev/tty3 > /dev/tty3\n#changing to VT 3 so that we can see whats going on....\n/usr/bin/chvt 3\n(\ncp -va /etc/resolv.conf /mnt/sysimage/etc/resolv.conf\n/usr/bin/chvt 1\n) 2>&1 | tee /mnt/sysimage/root/install.postnochroot.log\n<%= section_end -%>\n\n%post\nlogger "Starting anaconda <%= @host %> postinstall"\nexec < /dev/tty3 > /dev/tty3\n#changing to VT 3 so that we can see whats going on....\n/usr/bin/chvt 3\n(\n<% if subnet.respond_to?(:dhcp_boot_mode?) -%>\n<%= snippet \'kickstart_networking_setup\' %>\n<% end -%>\n\n#update local time\necho "updating system time"\n/usr/sbin/ntpdate -sub <%= @host.params[\'ntp-server\'] || \'0.fedora.pool.ntp.org\' %>\n/usr/sbin/hwclock --systohc\n\n<% if proxy_uri -%>\n# Yum proxy\necho \'proxy = <%= proxy_uri %>\' >> /etc/yum.conf\n<% end -%>\n\n<% if rhel_compatible && !@host.param_false?(\'enable-epel\') -%>\n<%= snippet \'epel\' -%>\n<% end -%>\n\n<% if @host.info[\'parameters\'][\'realm\'] && @host.realm && @host.realm.realm_type == \'FreeIPA\' -%>\n<%= snippet \'freeipa_register\' %>\n<% end -%>\n\n<% unless @host.param_false?(\'package_upgrade\') -%>\n# update all the base packages from the updates repository\nif [ -f /usr/bin/dnf ]; then\n  dnf -y update\nelse\n  yum -t -y update\nfi\n<% end -%>\n\n<%= snippet(\'remote_execution_ssh_keys\') %>\n\n<% if chef_enabled %>\n<%= snippet \'chef_client\' %>\n<% end -%>\n\n<% if puppet_enabled %>\n<% if @host.param_true?(\'enable-puppetlabs-pc1-repo\') || @host.param_true?(\'enable-puppetlabs-repo\') -%>\n<%= snippet \'puppetlabs_repo\' %>\n<% end -%>\n<%= snippet \'puppet_setup\' %>\n<% end -%>\n\n<% if salt_enabled %>\n<%= snippet \'saltstack_setup\' %>\n<% end -%>\n\n<% if @host.operatingsystem.name == \'OracleLinux\' && @host.param_true?(\'disable-uek\') -%>\n# Uninstall the Oracle Unbreakable Kernel packages\nyum -t -y remove kernel-uek*\nsed -e \'s/DEFAULTKERNEL=kernel-uek/DEFAULTKERNEL=kernel/g\' -i /etc/sysconfig/kernel\n<% end -%>\n\nsync\n\n<% if rhel_compatible -%>\nrm -f /etc/yum.repos.d/*\ncat > /etc/yum.repos.d/CentOS-Base.repo << \'EOF\'\n[base]\nname=CentOS-$releasever - Base\ngpgcheck=1\ngpgkey={0}/repos/pki/$basearch/RPM-GPG-KEY-CentOS-7\nbaseurl={0}/repos/centos/7/os/$basearch\n\n[update]\nname=CentOS-$releasever - Updates\ngpgcheck=1\ngpgkey={0}/repos/pki/$basearch/RPM-GPG-KEY-CentOS-7\nbaseurl={0}/repos/centos/7/updates/$basearch\nEOF\ncat > /etc/yum.repos.d/epel.repo << \'EOF\'\n[epel]\nname=Extra Packages for Enterprise Linux 7 - $basearch\nenabled=1\ngpgcheck=1\ngpgkey={0}/repos/pki/$basearch/RPM-GPG-KEY-EPEL-7\nbaseurl={0}/repos/epel/7/$basearch\nEOF\n<% end -%>\n<% if rhel_compatible -%>\n<% @host.interfaces.each do |i| %>\ntouch /etc/sysconfig/network-scripts/route-<%= i.identifier %>\ntouch /etc/sysconfig/network-scripts/rule-<%= i.identifier %>\n<% end -%>\n<% end -%>\n# Inform the build system that we are done.\necho "Informing Foreman that we are built"\nwget -q -O /dev/null --no-check-certificate <%= foreman_url(\'built\') %>\n) 2>&1 | tee /root/install.post.log\nexit 0\n\n<%= section_end -%>\n'.format(repo_url)

    kickstarter_default={'template': kickstart_str}

    kickstarter_pxelinux = { 'template': '<%#\nkind: PXELinux\nname: Kickstart default PXELinux\noses:\n- CentOS\n- Fedora\n- RedHat\n-%>\n# This file was deployed via \'<%= template_name %>\' template\n<%\nmajor = @host.operatingsystem.major.to_i\nmac = @host.provision_interface.mac\n# Tell Anaconda to perform network functions with boot interface\n#  both current and legacy syntax provided\noptions = ["network", "ksdevice=bootif", "ks.device=bootif"]\nif mac\nbootif = \'00-\' + mac.gsub(\':\', \'-\')\noptions.push("BOOTIF=#{bootif}")\nend\n# Tell Anaconda what to pass off to kickstart server\n#  both current and legacy syntax provided\noptions.push("kssendmac", "ks.sendmac", "inst.ks.sendmac")\n# handle non-DHCP environments (e.g. bootdisk)\nsubnet = @host.provision_interface.subnet\nunless subnet.dhcp_boot_mode?\n# static network configuration\nip = @host.provision_interface.ip\nmask = subnet.mask\ngw = subnet.gateway\ndns = [subnet.dns_primary]\nif subnet.dns_secondary != \'\'\ndns.push(subnet.dns_secondary)\nend\nif (@host.operatingsystem.name.match(/Fedora/i) && major < 17) || major < 7\n# old Anacoda found in Fedora 16 or RHEL 6 and older\ndns_servers = dns.join(\',\')\noptions.push("ip=#{ip}", "netmask=#{mask}", "gateway=#{gw}", "dns=#{dns_servers}")\nelse\noptions.push("ip=#{ip}::#{gw}:#{mask}:::none")\ndns.each { |server|\noptions.push("nameserver=#{server}")\n}\nend\nend\n# optional repository for Atomic\nif @host.operatingsystem.name.match(/Atomic/i)\noptions.push("inst.repo=#{@host.operatingsystem.medium_uri(@host)}")\nend\nif @host.params[\'blacklist\']\noptions.push("modprobe.blacklist=" + @host.params[\'blacklist\'].gsub(\' \', \'\'))\nend\nksoptions = options.join(\' \')\n-%>\nTIMEOUT <%= @host.params[\'loader_timeout\'] || 10 %>\nDEFAULT <%= template_name %>\nLABEL <%= template_name %>\nKERNEL <%= @kernel %>\nAPPEND initrd=<%= @initrd %> ks=<%= foreman_url(\'provision\') %> <%= pxe_kernel_options %> <%= ksoptions %> net.ifnames=0 biosdevname=0\nIPAPPEND 2\n'}

def ptable_init(ptables,ptable_sys):
  
    BOOT=ptables['boot']
    BOOTTYPE=BOOT['fstype']
    BOOTSIZE=BOOT['size']
    SWAP=ptables['swap']
    SWAPTYPE=SWAP['fstype']
    SWAPSIZE=SWAP['size']
    HOME=ptables['home']
    HOMETYPE=HOME['fstype']
    HOMESIZE=HOME['size']
    VAR=ptables['var']
    VARTYPE=VAR['fstype']
    VARSIZE=VAR['size']  
    TMP=ptables['tmp']
    TMPTYPE=TMP['fstype']
    TMPSIZE=TMP['size']
    ROOT=ptables['root']
    ROOTTYPE=ROOT['fstype']
    ROOTSIZE=ROOT['size']
    
    MINSIZE=ptable_sys['disk_minimum']
    BOOTSYSTEM=ptable_sys['boot_size']
    BTSYSTEMTYPE=ptable_sys['boot_type']
    SWAPSYSTEM=ptable_sys['swap_size']
    SWAPSYSTEMTYPE=ptable_sys['swap_type']
    HOMESYSTEM=ptable_sys['home_size']
    HOMESYSTEMTYPE=ptable_sys['home_type']
    VARSYSTEM=ptable_sys['var_size']
    VARSYSTEMTYPE=ptable_sys['var_type']
    TMPSYSTEM=ptable_sys['tmp_size']
    TMPSYSTEMTYPE=ptable_sys['tmp_type']
    ROOTSYSTEM=ptable_sys['root_size']
    ROOTSYSTEMTYPE=ptable_sys['root_type']
    snippet_str='<%#\nkind: ptable\nname: Kickstart default\noses:\n- CentOS\n- Fedora\n- RedHat\n%>\n\n#Dynamic\nDIR=\"/sys/block\"\nROOTDRIVE=\"\"\nisDefault=true\nfor DEV in sda sdb sdc sdd hda hdb; do\nif [ -d $DIR/$DEV ]; then\nREMOVABLE=`cat $DIR/$DEV/removable`\nif (( $REMOVABLE == 0 )); then\necho \'not removable disk: \' $DEV\nSIZE=`cat $DIR/$DEV/size`\nGB=$(($SIZE/2**21))\nif [ $GB -gt {24} ]; then\necho \"$(($SIZE/2**21))GB\"\nif [ -z $ROOTDRIVE ]; then\nROOTDRIVE=$DEV\nfi\nfi\nfi\nfi\ndone\nif [ $GB -lt {24} ]; then\nact_mem=$((`grep MemTotal: /proc/meminfo | sed \'s/^MemTotal: *//\'|sed \'s/ .*//\'` / 1024))\nif [ \"$act_mem\" -gt 2048 ]; then\nvir_mem=$(($act_mem + 2048))\nelse\nvir_mem=$(($act_mem * 2))\nfi\ncat <<EOF > /tmp/diskpart.cfg\nzerombr\nclearpart --all --initlabel\npart swap --size \"$vir_mem\" \npart /boot --fstype ext2 --size 750 --asprimary\npart / --fstype ext4 --size 1024 --grow --asprimary\nEOF\nelse\nMB=$(($SIZE/2/1024))\nBOOTMB=$(($MB*{0}/100))\nSWAPMB=$(($MB*{1}/100))\nHOMEMB=$(($MB*{2}/100))\nVARMB=$(($MB*{3}/100))\nTMPMB=$(($MB*{4}/100))\nROOTMB=$(($MB*{5}/100))\nfor _ in once; do\nif [ $BOOTMB -lt {6} ];\nthen\nbreak\nfi\nif [ $SWAPMB -lt {7} ];\nthen\nbreak\nfi\nif [ $HOMEMB -lt {8} ];\nthen\nbreak\nfi\nif [ $VARMB -lt {9} ];\nthen\nbreak\nfi\nif [ $TMPMB -lt {10} ];\nthen\nbreak\nfi\nif [ $ROOTMB -lt {11} ];\nthen\nbreak\nfi\ncat <<EOF > /tmp/diskpart.cfg\nzerombr\nclearpart --all --drives=$ROOTDRIVE --initlabel\nbootloader --location=mbr --driveorder=$ROOTDRIVE\npart pv.00 --grow --ondisk=$ROOTDRIVE\nvolgroup VolGroup00 pv.00\nlogvol swap --fstype {12} --size=$SWAPMB --name=swap --vgname=VolGroup00\npart /boot --fstype {13} --size=$BOOTMB --ondisk=$ROOTDRIVE\nlogvol /tmp --fstype {14} --size=$TMPMB --name=tmp --vgname=VolGroup00\nlogvol /var --fstype {15} --size=$VARMB --name=varlog --vgname=VolGroup00\nlogvol /home --fstype {16} --size=$HOMEMB --name=home --vgname=VolGroup00\nlogvol / --fstype {17} --size=1 --name=root --grow --vgname=VolGroup00\nEOF\nisDefault=false\ndone\nif [ \"$isDefault\" = true ]; then\ncat <<EOF > /tmp/diskpart.cfg\nzerombr\nclearpart --all --drives=$ROOTDRIVE --initlabel\nbootloader --location=mbr --driveorder=$ROOTDRIVE\npart pv.00 --grow --ondisk=$ROOTDRIVE\nvolgroup VolGroup00 pv.00\nlogvol swap --fstype {18} --size={7} --name=swap --vgname=VolGroup00\npart /boot --fstype {19} --size={6} --ondisk=$ROOTDRIVE\nlogvol /tmp --fstype {20} --size={10} --name=tmp --vgname=VolGroup00\nlogvol /var --fstype {21} --size={9} --name=varlog --vgname=VolGroup00\nlogvol /home --fstype {22} --size={8} --name=home --vgname=VolGroup00\nlogvol / --fstype {23} --size=1 --name=root --grow --vgname=VolGroup00\nEOF\nfi\nfi\n'.format(BOOTSIZE,SWAPSIZE,HOMESIZE,VARSIZE,TMPSIZE,ROOTSIZE,BOOTSYSTEM,SWAPSYSTEM,HOMESYSTEM,VARSYSTEM,TMPSYSTEM,ROOTSYSTEM,SWAPTYPE,BOOTTYPE,TMPTYPE,VARTYPE,HOMETYPE,ROOTTYPE,SWAPSYSTEMTYPE,BTSYSTEMTYPE,TMPSYSTEMTYPE,VARSYSTEMTYPE,HOMESYSTEMTYPE,ROOTSYSTEMTYPE,MINSIZE)
    ptable = { 'snippet': snippet_str }
    return ptable
