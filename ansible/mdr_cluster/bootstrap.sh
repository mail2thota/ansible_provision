#!/bin/bash
set -e
repo_url=$1
regex='(https?|ftp|file)://[-A-Za-z0-9\+&@#/%?=~_|!:,.;]*[-A-Za-z0-9\+&@#/%=~_|]'
red=`tput setaf 1`
green=`tput setaf 2`
reset=`tput sgr0`
bold=`tput bold`
if [[ $repo_url =~ $regex ]]
then 
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
	ansible-playbook mdr.yml
} 
option1="Node Provision"
option2="Cluster"
option3="Node Provision & Cluster"
option4="Quit"
PS3='Please enter your choice: '
options=("${option1}" "${option2}" "${option3}" "${option4}")
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
            exit 1
            ;;
        *) echo "${bold}${red}ERROR! Invalid option${reset}";;
    esac
done



