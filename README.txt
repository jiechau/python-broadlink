
original 
README_original.md
original
https://github.com/mjg59/python-broadlink


main.py (it's python fastapi)
providing entry points for homebridge webhook
=============================================

(1) root
# apt install python3.9
# apt install python3.9-venv

(2) user
cd $HOME/venv
/usr/bin/python3.9 -m venv --system-site-packages py39ir
source py39ir/bin/activate
pip3 install --upgrade pip

(3) copy config files
git clone https://github.com/jiechau/python-broadlink
cd python-broadlink
cp config_secrets_python-broadlink_example.yaml config_secrets_python-broadlink.yaml
# imports 
pip3 install pyyaml==6.0
pip3 install --upgrade pyopenssl cryptography
pip3 install fastapi uvicorn
pip3 install broadlink

(4) run (192.168.123.165 is host ip example)
uvicorn main:app --host 0.0.0.0 --port 8080
# 
GET http://192.168.123.165:8080/ping
#
POST http://192.168.123.165:8080/trigger
{
    "id": "switch_aircon_livingroom",
    "action": "on"
}

(5) homebridge setting

i use  homebridge:
https://github.com/homebridge/docker-homebridge
# i use docker, no docker compose
docker run --net=host --name=homebridge -v $(pwd)/homebridge:/homebridge homebridge/homebridge:latest
# add plugins http://<homebridge ip>:8581/
"homebridge-http-webhooks"
https://www.npmjs.com/package/homebridge-http-webhooks
# config setting for devices and config
http://<homebridge ip>:8581/config
example in config.json:
{
    "bridge": {
        "name": "Homebridge xxxx",
        "username": "0E:87:92:xx:xx:xx",
        "port": 51056,
        "pin": "111-11-11",
        "advertiser": "bonjour-hap"
    },
    "accessories": [],
    "platforms": [
        {
            "platform": "HttpWebHooks",
            "webhook_port": "51828",
            "switches": [
                {
                    "id": "switch_aircon_livingroom",
                    "name": "客廳冷氣",
                    "on_url": "http://192.168.123.165:8080/trigger",
                    "on_method": "POST",
                    "on_body": "{ \"id\": \"switch_aircon_livingroom\", \"action\": \"on\" }",
                    "on_headers": "{\"Content-Type\": \"application/json\"}",
                    "off_url": "http://192.168.123.165:8080/trigger",
                    "off_method": "POST",
                    "off_body": "{ \"id\": \"switch_aircon_livingroom\", \"action\": \"off\" }",
                    "off_headers": "{\"Content-Type\": \"application/json\"}"
                }
            ]
        },
        {
            "name": "Config",
            "port": 8581,
            "platform": "config"
        }
    ]
}


(6) misc
Homebridge
https://github.com/homebridge 
Homebridge Docker image 
https://github.com/homebridge/docker-homebridge
# i use docker, no docker compose
docker run --net=host --name=homebridge -v $(pwd)/homebridge:/homebridge homebridge/homebridge:latest
#
http://<homebridge ip>:8581/
use web UI to add plugins (recommend):
homebridge-cmdswitch2
homebridge-http-webhooks
# or by command line:
hb-service add homebridge-cmdswitch2



