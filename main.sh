#!/bin/bash
NOW=$(date +"%Y-%m-%d %H:%M:%S")
#
ff_pid=$(ps -ef | grep uvicorn | grep python-broadlink | grep -v 'grep' | awk '{print $2}')
kill -9 $ff_pid
echo $NOW 'stop fastapi python-broadlink processes' $ff_pid
#
echo $(date +"%Y-%m-%d %H:%M:%S") 'start fastapi python-broadlink processes'
cd $HOME/life_codes/python-broadlink
source .venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8080 >> $HOME/_ai_logs/python-broadlink/python-broadlink.log 2>&1 &
sleep 5
echo $(date +"%Y-%m-%d %H:%M:%S") ' process fastapi python-broadlink: '$(ps -ef | grep uvicorn | grep python-broadlink | grep -v grep | awk '{print $2}')
#
END=$(date +"%Y-%m-%d %H:%M:%S")
echo $END 'END (from' $NOW
echo ' '
