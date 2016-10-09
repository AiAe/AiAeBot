import discord
import json
import sys
import pprint
import urllib.request

client = discord.Client()

@client.event
async def on_ready():
    discordServer = None
    for i in client.servers:
        if i.id in conf["server"]:
            url = conf['url'].format("random", "", "")
            response = urllib.request.urlopen(url).read()
            await client.send_message(i.default_channel, str(response,'utf-8'))
    await client.logout()
    await client.close()

if __name__ == "__main__":
    try:
        with open("config.json", "r") as f:
            conf = f.read()
        conf = json.loads(conf)
    except:
        print("config???")
        raise
        sys.exit()

    client.run(conf["token"])