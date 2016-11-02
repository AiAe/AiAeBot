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

description = ''' AiAe Bot made by Daniel '''
bot = commands.Bot(command_prefix='.', description=description)

def __init__(self, bot):
    self.bot = bot

def is_owner_check(message):
    if message.author.id == conf['owner_permission']:
        return True
    else:
        return False

def is_owner():
    return commands.check(lambda ctx: is_owner_check(ctx.message))

def role_or_permissions(ctx, check):
    author = ctx.message.author

    role = discord.utils.find(check, author.roles)
    return role is not None

def admin_or_permissions():
    def predicate(ctx):
        return role_or_permissions(ctx, lambda r: r.name == 'Bot Commander')

    return commands.check(predicate)

async def shiping():
    await bot.wait_until_ready()
    channel = discord.Object(id='')
    # Works i guess ¯\_(ツ)_/¯
    while not bot.is_closed:
        atmhour = strftime("%I:%M", gmtime())
        if atmhour in ('01:00','02:00','03:00','04:00','05:00','06:00','07:00','08:00','09:00','10:00','11:00','12:00'):
            url = conf['url'].format("random", "", "")
            response = urllib.request.urlopen(url).read()
            await bot.send_message(channel, str(response,'utf-8'))
            #print("Sending ship... {}".format(atmhour))
        #print("Checking for time... {}".format(atmhour))
        await asyncio.sleep(60)

@bot.event
async def on_ready():
    await bot.change_status(game=discord.Game(name='with shipping people'))

@bot.command()
@admin_or_permissions()
async def ship(ship1 : str, ship2 : str):
    """ *.ship name1 name2 """
    url = conf['url'].format("ship", ship1, ship2)
    response = urllib.request.urlopen(url).read()
    await bot.say(str(response,'utf-8'), delete_after=10)

@bot.command()
@admin_or_permissions()
async def rship(ship1 : str, ship2 : str):
    """ *.rship name1 name2 """
    url = conf['url'].format("rship", ship1, ship2)
    response = urllib.request.urlopen(url).read()
    await bot.say(str(response,'utf-8'), delete_after=10)

@bot.command()
@commands.cooldown(1, 60, commands.BucketType.user)
async def ships():
    """ List with all ships """
    url = conf['url'].format("ships", "", "")
    response = urllib.request.urlopen(url).read()
    await bot.whisper("```" + str(response,'utf-8') + "```")

@bot.command()
@is_owner()
@commands.cooldown(1, 60, commands.BucketType.user)
async def setnick(ctx, nick : str):
    """ **Change bot nick """
    me = ctx.message.server.me
    await bot.change_nickname(me, nick)
    await bot.say(":ok_hand:")

@bot.command()
@is_owner()
@commands.cooldown(1, 60, commands.BucketType.user)
async def status(newgame : str):
    """ **Change bot status """
    await bot.change_status(game=discord.Game(name=newgame))
    await bot.say(":ok_hand:", delete_after=10)

@bot.command()
@admin_or_permissions()
@commands.cooldown(1, 360, commands.BucketType.user)
async def shipnow():
    """ *Ship now """
    url = conf['url'].format("random", "", "")
    response = urllib.request.urlopen(url).read()
    await bot.say(str(response,'utf-8'))
    
@bot.command()
@commands.cooldown(1, 60, commands.BucketType.user)
async def mf(fname : str):
    """ .mf name"""
    channel = ''
    # Need to rewrite
    if fname == "4oba":
        await bot.send_file(discord.Object(id=channel), './fingers/4oba.png')
    elif fname == "flanster":
        await bot.send_file(discord.Object(id=channel), './fingers/flanster.jpg')
    elif fname == "asdasd":
        await bot.send_file(discord.Object(id=channel), './fingers/asd.jpg')
    elif fname == "chugleader":
        await bot.send_file(discord.Object(id=channel), './fingers/chugleader.jpg')
    elif fname == "lexi":
        await bot.send_file(discord.Object(id=channel), './fingers/lexi.jpg')
    else:
        await bot.say("404 Middle Finger not found!")
@bot.command()
@is_owner()
async def shutdown():
    """ **Shutdown bot """
    await bot.say(":wave:")
    await bot.logout()
    await bot.close()

@bot.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def kys(*text):
    """ .kys text """
    # print(str(text))
    cleverbot_client = cleverbot.Cleverbot()
    answer = cleverbot_client.ask(str(text))
    await bot.say(answer)

if __name__ == "__main__":
    try:
        with open("./config_ships.json", "r") as f:
            conf = f.read()
        conf = json.loads(conf)
    except:
        print("config???")
        raise
        sys.exit()
    bot.loop.create_task(shiping())
    bot.run(conf["token"])