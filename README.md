# pySSHChat
SSH chat server written on Python3

![pySSHChat](https://github.com/LexSerest/pySSHChat/blob/master/img/record.gif?raw=true)

## TODO
- Switch line/ui mode
- Add commands for admin
- etc.

## Install
```bash
pip3 install pysshchat
```

## Run
```bash
# Listen default 2200 port and auto generated host key
python3 -m pysshchat

# Starting in daemon mode
python3 -m pysshchat --daemon

# Stopping for daemon mode
python3 -m pysshchat --stop

# Set listen 2222 port and set path server key
python3 -m pysshchat -p 2222 -k ~/.ssh/id_rsa

# Set password for connect to chat
python3 -m pysshchat --password YouPassword

# Load config file (see yaml/config.yaml)
python3 -m pysshchat --config <path>

# Set title
python3 -m pysshchat --set-title "You text"

# Set help text
python3 -m pysshchat --set-help "You text"
python3 -m pysshchat --set-help-file <path>

# Load you commands
python3 -m pysshchat --load-commands <path folder>

# Load all text (see yaml/text.yaml)
python3 -m pysshchat --load-text <path>
```
