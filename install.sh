#!/bin/bash

if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root through sudo." 1>&2
   exit 1
fi

RUNASUSER="sudo -u $SUDO_USER"

yum -y install python-devel python-pip python-virtualenv


virtualenv env
source ./env/bin/activate
pip install django
deactivate

