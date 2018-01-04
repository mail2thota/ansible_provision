#!/bin/bash
set -e
repo_url=$1
regex='(https?|ftp|file)://[-A-Za-z0-9\+&@#/%?=~_|!:,.;]*[-A-Za-z0-9\+&@#/%=~_|]'
red=`tput setaf 1`
green=`tput setaf 2`
reset=`tput sgr0`
bold=`tput bold`

cp -f  config.yml ./roles/pre-config/
if [[ $repo_url =~ $regex ]]
then
   if [ -w /etc/yum.conf ]; then
       sed -i "/^proxy=.*/d" /etc/yum.conf
       unset http_proxy
       unset https_proxy
       unset no_proxy
       unset HTTP_PROXY
       unset HTTPS_PROXY
       unset NO_PROXY
   fi 
   export repo_url
   echo "${bold}${green}Repository url is set as ${repo_url}${reset}"
else
   echo "${bold}${red}ERROR! Repository url is not valid${reset}"
   exit 1
fi
init(){
        thisdir=`dirname $0`
	source ${thisdir}/ansible_epel
	if [[ $EUID -ne 0 ]]; then
	  echo "You must be a root user" 2>&1
	  exit 1
	fi
	setBaseRepo
	setEpelRepo
	yum clean all
        echo "install ansible"
	yum install ansible -y
	#gnome-terminal -x ./lnav-0.8.2/lnav /var/log/ansible.*
}

foreman(){
	echo "execution of foreman playbook"
        ansible-playbook foreman.yml 
}

validate(){
        echo "Validating Config files"
	ansible-playbook validate.yml --tags=$1
}

ambari_hdp(){
	echo "execution of ambari and hdp playbook"
	rm -f ./roles/pre-config/config.yml
	cp config.yml ./roles/pre-config/
	ansible-playbook  mdr.yml
} 

updatehdp(){ 
	rm -f ./roles/updatehdp/update_hdp_cluster.yml
	cp update_hdp_cluster.yml ./roles/updatehdp/
        ansible-playbook updatehdp.yml --tags=config
        ansible-playbook updatehdp.yml --tags=hdp-install 
}

option1="Node Provision"
option2="Cluster"
option3="Node Provision & Cluster"
option4="Add/Remove hosts"
option5="Quit"
PS3='Please enter your choice: '
options=("${option1}" "${option2}" "${option3}" "${option4}" "${option5}")
select opt in "${options[@]}"
do
    case $opt in
        "${option1}")
            echo "${bold}${green}Selected ${option1}${reset}"
            init
	    validate foreman
            foreman
            break
            ;;
        "${option2}")
            echo "${bold}${green}Selected ${option2}${reset}"
	    init
            validate mdr
            ambari_hdp
            break
            ;;
        "${option3}")
            echo "${bold}${green}Selected ${option3}${reset}"
            init
            validate mdr,foreman
            foreman
            ambari_hdp
            break
            ;;
        "${option4}")
            echo "${bold}${green}Selected ${option4}${reset}"
            init
            updatehdp
            break
            ;;
         "${option5}")
            exit 1
            ;;
        *) echo "${bold}${red}ERROR! Invalid option${reset}";;
    esac
done



