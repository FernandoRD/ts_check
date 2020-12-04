#!/bin/bash

SESSION_DISPLAY=""
HOST=""
USER=""
PASSWORD=""
EXECUTABLE=""
RESILIENCE=""
CONFIDENCE_VALUE=""
SYSUSER=nagios

while getopts H:u:p:x:r:c:d: opt 
do
	case "$opt" in
		H) HOST=$OPTARG;;
		u) USER=$OPTARG;;
		p) PASSWORD=$OPTARG;;
		x) EXECUTABLE=$OPTARG;;
		r) RESILIENCE=$OPTARG;;
		c) CONFIDENCE_VALUE=$OPTARG;;
		d) SESSION_DISPLAY=$OPTARG;;
	esac 

done

export DISPLAY=:$SESSION_DISPLAY.0

sudo xinit -- :$SESSION_DISPLAY & >/dev/null 2>&1

sudo mv /root/.Xauthority /root/old.Xauthority
sudo touch /root/.Xauthority
sudo xauth generate :$SESSION_DISPLAY . trusted
#sudo xauth add ${HOST}:0 /root/. $(xxd -l 16 -p /dev/urandom)

sudo cp /root/.Xauthority /home/nagios/.Xauthority
sudo chown nagios.nagios /home/nagios/.Xauthority

#sudo startx & >/dev/null 2>&1


#source /home/nagios/tscheck/venv/bin/activate

sudo python3 /home/nagios/tscheck/ts_check.py -H $HOST -u $USER -p $PASSWORD -x $EXECUTABLE -r $RESILIENCE -c $CONFIDENCE_VALUE 2>/dev/null 
estado_exec=$?

ps -ef | grep xinit | grep -v grep | awk '{print $2}' | sudo xargs kill 

sleep 5

#echo $estado_exec
exit $estado_exec

