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
	is_shell_login=$(shopt -q login_shell && echo 'yes' || echo 'no')
	if [ "$DESKTOP_SESSION" = "gnome-classic" -a "$is_shell_login" == "no" ]
	then
 	   sudo gnome-terminal -x ./lnav-0.8.2/lnav /var/log/ansible.*
	fi
}

passwordFm()
{
    echo "Enter Foreman Authentication"
    read -p "Username: " fmusername
    while true; do
        read -s -p "Password: " fmpassword
        echo
        read -s -p "Password (again): " fmpassword2
        echo
        [ "$fmpassword" = "$fmpassword2" ] && break
        echo "Please try again"
    done
    echo
}

passwordNodes()
{
    echo "Enter Nodes Password"
    echo "Minimum 8 characters required"
    while true; do
        read -s -p "Password: " nodepassword
        echo
        read -s -p "Password (again): " nodepassword2
        echo
        len=`echo ${#nodepassword}`
        if [[ $len -ge 8 ]] ; then
            [ "$nodepassword" = "$nodepassword2" ] && break
        fi
        echo "password length should be greater than or equal 8 and must be match"
        echo "Please try again"
    done
    echo
}

passwordAccess()
{
    echo "Enter Nodes Username and Password"
    read -p "Username: " nodeusername
    read -s -p "Password: " nodepassword
    echo
}

passwordAmbari()
{
    echo "Enter Ambari Authentication"
    read -p "Username: " ambusername
    read -s -p "Password: " ambpassword
    echo
}

passwordHDP()
{
    echo "Enter HDP Password"
    while true; do
        read -s -p "Password: " hdppassword
        echo
        read -s -p "Password (again): " hdppassword2
        echo
        [ "$hdppassword" = "$hdppassword2" ] && break
        echo "Please try again"
    done
    echo
}

foreman(){
	echo "execution of foreman playbook"
        ansible-playbook foreman.yml --extra-vars "fmusername=$fmusername
        fmpassword=$fmpassword nodepass=$nodepassword" 
}

validate(){
        echo "Validating Config files"
	ansible-playbook validate.yml --tags=$1 
}

ambari_hdp(){
	rm -f ./roles/pre-config/config.yml
	cp config.yml  ./roles/pre-config/
	echo "execution of ambari and hdp playbook"
	ansible-playbook mdr.yml --extra-vars "ambari_user=admin
        ambari_password=admin hdp_password=$hdppassword ansible_user=$nodeusername
        ansible_ssh_pass=$nodepassword" 
}

updatehdp(){ 
	rm -f ./roles/updatehdp/update_hdp_cluster.yml
	cp update_hdp_cluster.yml ./roles/updatehdp/
        ansible-playbook updatehdp.yml --tags=config --extra-vars "ambari_user=$ambusername
        ambari_password=$ambpassword ansible_user=root
        ansible_ssh_pass=$nodepassword"
        ansible-playbook updatehdp.yml --tags=hdp-install --extra-vars "ambari_user=$ambusername
        ambari_password=$ambpassword ansible_user=root
        ansible_ssh_pass=$nodepassword"
} 

updateelasticsearch(){
        rm -f ./roles/updateelasticsearch/update_es_cluster.yml
        cp update_es_cluster.yml ./roles/updateelasticsearch
        echo "[es_add]" > ./inventory/hosts
        ansible-playbook configescluster.yml --tags config --extra-vars "ansible_user=root ansible_ssh_pass=$nodepassword"
        ansible-playbook updateescluster.yml --tags es-install --extra-vars "ansible_user=root ansible_ssh_pass=$nodepassword"

}

option1="Node Provision"
option2="Cluster"
option3="Node Provision & Cluster"
option4="Add/Remove hdp worker nodes"
option5="Add/Remove elasticsearch worker nodes"
option6="Quit"

PS3='Please enter your choice: '
options=("${option1}" "${option2}" "${option3}" "${option4}" "${option5}" "${option6}")
select opt in "${options[@]}"
do
    case $opt in
        "${option1}")
            echo "${bold}${green}Selected ${option1}${reset}"
            passwordFm
            passwordNodes
            init
	    validate foreman
            foreman
            break
            ;;
        "${option2}")
            echo "${bold}${green}Selected ${option2}${reset}"
            passwordHDP
            passwordAccess
            init
            validate mdr
            ambari_hdp
            break
            ;;
        "${option3}")
            echo "${bold}${green}Selected ${option3}${reset}"
            passwordFm
            passwordHDP
            passwordNodes
            init
            validate mdr,foreman
            foreman
            ambari_hdp
            break
            ;;
        "${option4}")
            echo "${bold}${green}Selected ${option4}${reset}"
            passwordAmbari
            passwordAccess
            init
            updatehdp
            break
            ;;
        "${option5}")
            echo  "${bold}${green}Selected ${option5}${reset}"
            passwordNodes
            init
            updateelasticsearch
            break
            ;;
        "${option666666}")
            exit 1
            ;;
        *) echo "${bold}${red}ERROR! Invalid option${reset}";;
    esac
done



