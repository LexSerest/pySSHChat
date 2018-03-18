# pySSHChat
Replace [jsSSHChat](https://github.com/LexSerest/pySSHChat) on Python3 (while without ncurses)

## TODO
- use ncurses
- Add info for create custom commands
- etc.

## Install
```bash
pip3 install pysshchat
```

## Run
```bash
 # Listen default 2200 port
python3 -m pysshchat

# Set listen 2222 port and set path server key
python3 -m pysshchat -p 2222 -k ~/.ssh/id_rsa

# Set path server key
python3 -m pysshchat -k ~/.ssh/id_rsa

# Load config file (see yaml/config.yaml)
python3 -m pysshchat --config <path>

# Set message welcome
python3 -m pysshchat --set-motd "You text"
python3 -m pysshchat --set-motd-file <path>

# Set help text
python3 -m pysshchat --set-help "You text"
python3 -m pysshchat --set-help-file <path>

# Load you commands
python3 -m pysshchat --load-commands <path folder>

# Load all text (see yaml/text.yaml)
python3 -m pysshchat --load-text <path>
```
