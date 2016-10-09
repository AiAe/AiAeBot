# shipsBot

### Requirements
- Python 3.5
- discord.py

### Discord
- Create two bots in https://discordapp.com/developers/applications/me
- Invite them in the server by 
```
https://discordapp.com/oauth2/authorize?client_id=BOT_CLIENT_ID&scope=bot&permissions=0
```
change BOT_CLIENT_ID with the bot ID.

### Server setup
- Create new database
- Upload SQL
- Edit in index.php from line 2 to 5

### Installation
```
$ pip install -r requirements.txt
```

- Edit config file

- Set up a cronjob that will send random ship every 1 hour.
```
0 * * * * python3 ship.py
```

### Extra
If interested in MelanzanaBot
https://git.zxq.co/Nyo/MelanzanaBot
