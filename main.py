from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import PlainTextResponse


# config
import yaml
def get_myconfig(_myconfig_file):
    ## read custom params from config.yaml
    with open(_myconfig_file, 'r', encoding="utf-8") as stream:
        _myconfig = yaml.load(stream, Loader=yaml.CLoader)
    return _myconfig
myconfig = get_myconfig("config_secrets_python-broadlink.yaml")
BLSH = myconfig['broadlink']['BLSH']
telegram_url = myconfig['telegram']['url']
chat_id = myconfig['telegram']['chat_id']


# use a telegram to test
import requests
requests.packages.urllib3.disable_warnings()
import json
def send_telegram_message(_id, _action):
    #telegram_url = 'https://api.telegram.org/bot666111111:AAFHp3SQNqTyKyc1111111/sendMessage'
    headers = {'Content-type': 'application/json'}
    #payload = json.dumps({"chat_id": "1111111","text": _id + "_" + _action})
    payload = json.dumps({"chat_id": chat_id, "text": _id + "_" + _action})
    response = requests.post(telegram_url, data=payload, headers=headers, verify=False)
    return

# use exec to test
import subprocess
def exec_subprocess(_id, _action):
    command = ["/bin/echo", _id, _action]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    # CompletedProcess(args=['/bin/echo', 'pushbutton_web', 'null'], returncode=0, stdout='pushbutton_web null\n', stderr='')
    print("return code:", result.returncode)
    return

# broadlink exec
import subprocess
def broadlink_subprocess(_id, _action):
    # $BCMD --device @/home/pi/eye_pb/em1 --send @/home/pi/eye_pb/pb_off
    if _id not in myconfig['webhooks']['em']:
        return
    if myconfig['webhooks']['em'][_id] not in myconfig['broadlink']['em_files']:
        return
    em_this = myconfig['broadlink']['em_files'][myconfig['webhooks']['em'][_id]]
    sg_this = myconfig['broadlink']['signal_files'][myconfig['webhooks']['sg'][_id + '_' + _action]]
    command = [BLSH, em_this, sg_this]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    #print("return code:", result.returncode)
    print("result:", result.stdout)
    return

# broadlink exec, for broadlink_subprocess_mechanicalswitch
import subprocess
import time
def broadlink_subprocess_mechanicalswitch(_id, _action):
    # $BCMD --device @/home/pi/eye_pb/em1 --send @/home/pi/eye_pb/pb_off
    if _id not in myconfig['webhooks']['em']:
        return
    if myconfig['webhooks']['em'][_id] not in myconfig['broadlink']['em_files']:
        return
    em_this = myconfig['broadlink']['em_files'][myconfig['webhooks']['em'][_id]]
    sg_this = myconfig['broadlink']['signal_files'][myconfig['webhooks']['sg'][_id + '_' + _action]]
    command = [BLSH, em_this, sg_this]
    push_times = 10 # for 'on' and 'push'
    if _action == 'off':
        push_times = 2
    '''
    "pushbuttons": [
                {
                    "id": "pushbutton_mechanicalswitch_go",
                    "name": "客廳電燈",
                    "push_url": "http://intra-ubuntu.jiechau.idv.tw:8080/trigger",
                    "push_method": "POST",
                    "push_body": "{ \"id\": \"pushbutton_mechanicalswitch_go\", \"action\": \"push\"  }",
                    "push_headers": "{\"Content-Type\": \"application/json\"}"
                },

    '''
    for i in range(push_times):
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        #time.sleep(0.7)
        #print(i)
    #print("return code:", result.returncode)
    print("result:", result.stdout)
    return

app = FastAPI()

# disable /favicon.ico
@app.get("/favicon.ico", include_in_schema=False)
async def disable_favicon():
    pass

@app.get("/ping")
async def ping():
    return PlainTextResponse("OK")

@app.post("/trigger", response_model=dict)
async def trigger(request: Request):
    input_data = await request.json()
    do_id = 'null'
    do_action = 'null'
    if 'id' in input_data:
        do_id = input_data['id']
    if 'action' in input_data:
        do_action = input_data['action']
    
    # 客廳電燈
    if do_id == 'pushbutton_mechanicalswitch_go':
        broadlink_subprocess_mechanicalswitch(do_id, do_action)
        return {"success": True, "id": do_id}

    #print(do_id, do_action)
    # test
    #send_telegram_message(do_id, do_action)
    # test
    #exec_subprocess(do_id, do_action)
    # broadlink exec
    else:
        broadlink_subprocess(do_id, do_action)
        return {"success": True, "id": do_id}

@app.post("/telegram", response_model=dict)
async def telegram(request: Request):
    input_data = await request.json()
    do_id = 'null'
    do_action = 'null'
    if 'id' in input_data:
        do_id = input_data['id']
    if 'action' in input_data:
        do_action = input_data['action']
    #print(do_id, do_action)
    # test
    send_telegram_message(do_id, do_action)
    # test
    #exec_subprocess(do_id, do_action)
    # broadlink exec
    #broadlink_subprocess(do_id, do_action)
    return {"success": True, "id": do_id}

@app.post("/exec", response_model=dict)
async def execute_action(request: Request):
    input_data = await request.json()
    do_id = 'null'
    do_action = 'null'
    if 'id' in input_data:
        do_id = input_data['id']
    if 'action' in input_data:
        do_action = input_data['action']
    #print(do_id, do_action)
    # test
    #send_telegram_message(do_id, do_action)
    # test
    exec_subprocess(do_id, do_action)
    # broadlink exec
    #broadlink_subprocess(do_id, do_action)
    return {"success": True, "id": do_id}
