#!/bin/bash

export DISPLAY=:0.0

HOST=""
USER=""
PASSWORD=""
EXECUTABLE=""
RESILIENCE=""
CONFIDENCE_VALUE=""
SYSUSER=nagios

while getopts H:u:p:x:r:c: opt 
do
	case "$opt" in
		H) HOST=$OPTARG;;
		u) USER=$OPTARG;;
		p) PASSWORD=$OPTARG;;
		x) EXECUTABLE=$OPTARG;;
		r) RESILIENCE=$OPTARG;;
		c) CONFIDENCE_VALUE=$OPTARG;;
	esac 

done
shift $((OPTIND-1))

BROKEN_LINK=`find -L /home/$SYSUSER -maxdepth 1 -type l | tr -d '\n'`
echo "-------------------------" >> /tmp/script.log
echo $BROKEN_LINK >> /tmp/script.log
echo "-------------------------" >> /tmp/script.log
echo ${#BROKEN_LINK} >> /tmp/script.log
echo "-------------------------" >> /tmp/script.log

if [ ${#BROKEN_LINK} -gt 0 ];
then
	echo "executou bronken link" >> /tmp/script.log
	sudo rm $BROKEN_LINK
	sudo chmod 777 /var/run/gdm	
	ln -s /var/run/gdm/`ls /var/run/gdm/ | grep nagios`/database /home/nagios/.Xauthority 
	exit
fi

source /home/nagios/tscheck/venv/bin/activate
python3 /usr/local/nagios/libexec/ts_check.py -H $HOST -u $USER -p $PASSWORD -x $EXECUTABLE -r $RESILIENCE -c $CONFIDENCE_VALUE 2> /dev/null 

