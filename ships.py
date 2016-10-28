import discord
import json
import sys
import pprint
import urllib.request
from discord.ext import commands
import cleverbot
import time
import asyncio
from time import gmtime, strftime

description = ''' Ships bot '''
bot = commands.Bot(command_prefix='.', description=description)

def __init__(self, bot):
    self.bot = bot

def is_moderator_check(message):
    for i in range(0, len(conf['commands_permission'])):
        if message.author.id == str(conf['commands_permission'][i]):
            return True

def is_owner_check(message):
    if message.author.id == conf['owner_permission']:
        return True
    else:
        return False

def is_moderator():
    return commands.check(lambda ctx: is_moderator_check(ctx.message))

def is_owner():
    return commands.check(lambda ctx: is_owner_check(ctx.message))

async def shiping():
    await bot.wait_until_ready()
    channel = discord.Object(id='')
    while not bot.is_closed:
        # I guess this will do the job :D
        atmhour = strftime("%I:%M", gmtime())
        if atmhour in ('01:00','02:00','03:00','04:00','05:00','06:00','07:00','08:00','09:00','10:00','11:00','12:00'):
            url = conf['url'].format("random", "", "")
            response = urllib.request.urlopen(url).read()
            await bot.send_message(channel, str(response,'utf-8'))
        # print(atmhour)
        await asyncio.sleep(60)

@bot.event
async def on_ready():
    await bot.change_status(game=discord.Game(name='with shipping people'))

@bot.command(hidden=True)
@is_moderator()
async def ship(ship1 : str, ship2 : str):
    url = conf['url'].format("ship", ship1, ship2)
    response = urllib.request.urlopen(url).read()
    await bot.say(str(response,'utf-8'), delete_after=10)

@bot.command(hidden=True)
@is_moderator()
async def rship(ship1 : str, ship2 : str):
    url = conf['url'].format("rship", ship1, ship2)
    response = urllib.request.urlopen(url).read()
    await bot.say(str(response,'utf-8'), delete_after=10)

@bot.command()
async def ships():
    url = conf['url'].format("ships", "", "")
    response = urllib.request.urlopen(url).read()
    await bot.say("```" + str(response,'utf-8') + "```", delete_after=10)

@bot.command(pass_context=True, no_pm=True, hidden=True)
@is_owner()
async def setnick(ctx, nick : str):
    me = ctx.message.server.me
    await bot.change_nickname(me, nick)
    await bot.say(":ok_hand:")

@bot.command(hidden=True)
@is_owner()
async def status(newgame : str):
    await bot.change_status(game=discord.Game(name=newgame))
    await bot.say(":ok_hand:", delete_after=10)

@bot.command(hidden=True)
@is_moderator()
async def shipnow():
    url = conf['url'].format("random", "", "")
    response = urllib.request.urlopen(url).read()
    await bot.say(str(response,'utf-8'))

@bot.command(hidden=True)
@is_owner()
async def shutdown():
    await bot.say(":wave:")
    await bot.logout()
    await bot.close()

@bot.command()
async def kys(text : str):
    cleverbot_client = cleverbot.Cleverbot()
    answer = cleverbot_client.ask(text)
    await bot.say(answer)

if __name__ == "__main__":
    try:
        with open("./config.json", "r") as f:
            conf = f.read()
        conf = json.loads(conf)
    except:
        print("config???")
        raise
        sys.exit()
    bot.loop.create_task(shiping())
    bot.run(conf["token"])