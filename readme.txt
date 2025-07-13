python 3.9


這裡紀錄一下流程


***************************************************************
在 homebridge (目前是一個 docker image) 有定義它要呼叫的 trigger 位置
從定義檔可以看出來 http://<homebridge ip>:8581/
(http://192.168.123.163:8581/ 或 http://192.168.123.163:8581/)
定義檔 內 用
http://intra-ubuntu.jiechau.idv.tw:8080/trigger

所以需要 intra-ubuntu.jiechau.idv 是 192.168.123.166 


****************************************************************
這個 python-broadlink

python 3.9 
用 requirements_py39ir.txt
需要 config_secrets_python-broadlink.yaml

做 2 件事

1.
這個 fastapi 接受 /trigger
然後呼叫自己的 BLSH (定義在 config_secrets_python-broadlink.yaml)
BLSH: /home/jie/life_codes/python-broadlink/cli/broadlink_cli.sh

2.
broadlink_cli.sh 
broadlink_cli.sh 的 $script_dir 是 $HOME/life_codes/python-broadlink/cli
裡面也會需要 python venv 用同一個 .venv:
cd $script_dir/..
source .venv/bin/activate

todo: broadlink_cli.sh 需要寫下測試的指令 例如用一個 簡單的冷氣







