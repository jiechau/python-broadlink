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
    #print(do_id, do_action)
    # test
    send_telegram_message(do_id, do_action)
    # test
    exec_subprocess(do_id, do_action)
    return {"success": True, "id": do_id}

