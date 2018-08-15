# pySSHChat
SSH chat server written in python3

![pySSHChat](https://github.com/LexSerest/pySSHChat/blob/master/img/record.gif?raw=true)

## Features
- Formating text
- Admin function
- Simply and Urwid mode
- Automatic key generation

## Installation
```bash
pip3 install pysshchat
```

## Usage

### Administrator
For administration - add your login and MD5 hash of the public key to the configuration file
You also get administrator rights if you are logged in with localhost

__Show MD5 hash public key__

`ssh-keygen -E md5 -lf ~/.ssh/id_rsa.pub`

__Example config.yaml file for administration__

```
admin:
  mylogin: "ce:ff:b1:c3:da:09:ab:ff:99:00:9b:b4:3d:5b:91:18"
```

### Commands
```
/help or F1 - help
/color or F2 - change you color
/list or F3 - show online user
/me <you message> - write in the third person
/quit - exit

# Only admins command
/kick <username>
/ban <username> - ban user by ip (only temporarily)
/unban <username> - unban user
/info <username> - get time connect, user IP address, etc.
```

### Connect to chat
```
# Auto mode selection
# if the size of the terminal is less than 60x15 - used the simple mode
# if environment is empty - used the simple mode (for mobile client)
ssh <host> -p <port>

# Connect on urwid mode
SIMPLE=0 ssh -o SendEnv=SIMPLE <host> -p <port>

# Connect on simple mode
SIMPLE=1 ssh -o SendEnv=SIMPLE <host> -p <port>
```

### Formating text
```
#b# - bold
#i# - italics
#u# - underline
#0-255# - 8-bit color
#-# - reset
```

## Run
```bash
# Listen default 127.0.0.1:2200 and auto generated host key
pysshchat

# Set listen 2222 port and set path server key
pysshchat -p 2222 -k ~/.ssh/id_rsa

# Set password for connect to chat
pysshchat --password YouPassword

# Only simply mode (not use urwid)
pysshchat --only-simply-mode

# Load config file (see yaml/config.yaml)
pysshchat --config <path>

# Set title
pysshchat --set-title "You text"

# Set help text
pysshchat --set-help "You text"
pysshchat --set-help-file <path>

# Load all text (see yaml/text.yaml)
pysshchat --load-text <path>
```


## BUGS
- urwid mode heavily loads the processor 🤔
- urwid mode works in a single thread and is not asynchronous 🤔

## TODO
- More commands
- More info
- Refactoring
- Daemon mode
- etc.
