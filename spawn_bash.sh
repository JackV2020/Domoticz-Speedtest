#!/bin/bash
#
# This script is used by the plugin to run the commands in a spawned processes
#
# Make sure protection mask of created files is -rw-rw-rw-
#
#set -x
umask 0000
#
# location of this script
#
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
#
# construct the command
#
cd $DIR
$DIR/$1 $2 $3 $4 $5 $6 $7 $8 $9 ${10} ${11} ${12} ${13} ${14} ${15} ${16} ${17} ${18} ${19} ${20} ${21}> /dev/null 2>&1 &
