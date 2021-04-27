#!/usr/bin/bash
#
# file      : speedtest.sh
# author    : J Veraart
# receives  : idx for ping speed, uplink speed, downlink speed, file upload and file download speed
# returns   : stores data in domoticz using received idxes
# usage     : started by plugin.py "Jacks Speedtest" via spawn_bash.sh 
# REQUIREMENTS : 
#
#   1 speedtest.py which I included by : wget https://raw.githubusercontent.com/sivel/speedtest-cli/master/speedtest.py
#   2 when you have users and passwords make an exception for you host address in the Domoticz Setup
#
do_it(){
#
# go to this scripts directory
#
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $DIR
#
# gather data which takes a while
#
SPEEDDATA=$(./speedtest.py  --secure --simple)
speed_ping=$( echo $SPEEDDATA | cut -d " " -f 2)
speed_download=$( echo $SPEEDDATA | cut -d " " -f 5)
speed_upload=$(   echo $SPEEDDATA | cut -d " " -f 8)
#
SPEEDDATA=$(./speedtest.py  --secure --simple --single)
speed_single_download=$( echo $SPEEDDATA | cut -d " " -f 5)
speed_single_upload=$( echo $SPEEDDATA | cut -d " " -f 8)
#
# show data or send data to domoticz
#
if [[ $1 == '' ]]
then
    echo "ping          $speed_ping"
    echo "up link       $speed_upload"
    echo "down link     $speed_download"
    echo "upload file   $speed_single_upload"
    echo "download file $speed_single_download"
else
    wget -q --delete-after "http://"`hostname`":8080/json.htm?type=command&param=udevice&idx=$1&svalue=$speed_ping"
    wget -q --delete-after "http://"`hostname`":8080/json.htm?type=command&param=udevice&idx=$2&svalue=$speed_upload"
    wget -q --delete-after "http://"`hostname`":8080/json.htm?type=command&param=udevice&idx=$3&svalue=$speed_download"
    wget -q --delete-after "http://"`hostname`":8080/json.htm?type=command&param=udevice&idx=$4&svalue=$speed_single_upload"
    wget -q --delete-after "http://"`hostname`":8080/json.htm?type=command&param=udevice&idx=$5&svalue=$speed_single_download"
fi
}
#
# use a sub so you can optionally save some output.
#
do_it $1 $2 $3 $4 $5 # >> /home/pi/domoticz/plugins/speedtest/speedtest.log
#
# did_it ;-)
#
