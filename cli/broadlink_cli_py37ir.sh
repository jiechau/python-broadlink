#!/bin/bash

if [ "$#" -ne 2 ]; then
  #return
  exit
fi

em=$1
sg=$2
echo @${em} @${sg}

# Get the full path to the script using realpath
script_path=$(realpath "${BASH_SOURCE[0]}")
# Resolve the directory component of the path
script_dir=$(dirname "$script_path")
echo $script_dir


cd $HOME/venv
source py37ir/bin/activate
cd $script_dir

# $BCMD --device @/home/pi/eye_pb/em1 --send @/home/pi/eye_pb/pb_off
$script_dir/broadlink_cli --device @${em} --send @${sg}
#$script_dir/broadlink_discovery

deactivate

