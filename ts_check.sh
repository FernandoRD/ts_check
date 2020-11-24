#!/bin/bash

HOST=""
USER=""
PASSWORD=""
EXECUTABLE=""
RESILIENCE=""
CONFIDENCE_VALUE=""
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

BROKEN_LINK=""
BROKEN_LINK=`find -L /root -type l`

if [ $BROKEN_LINK!="" ];
then
	rm $BROKEN_LINK
	
	ln -s /var/run/gdm/`ls /var/run/gdm/ | grep fernando`/database /root/.Xauthority
fi


DISPLAY=:0.0 /home/fernando/tscheck/ts_check.py -H $HOST -u $USER -p $PASSWORD -x $EXECUTABLE -r $RESILIENCE -c $CONFIDENCE_VALUE 
