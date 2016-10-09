import discord
import json
import sys
import pprint
import urllib.request
from discord.ext import commands

description = ''' Ships bot '''
bot = commands.Bot(command_prefix='!', description=description)

def is_owner_check(message):
    return message.author.id == ''

def is_owner():
    return commands.check(lambda ctx: is_owner_check(ctx.message))

@bot.command()
async def ship(ship1 : str, ship2 : str):
    url = conf['url'].format("ship", ship1, ship2)
    response = urllib.request.urlopen(url).read()
    await bot.say(str(response,'utf-8'))

@bot.command()
async def rship(ship1 : str, ship2 : str):
    url = conf['url'].format("rship", ship1, ship2)
    response = urllib.request.urlopen(url).read()
    await bot.say(str(response,'utf-8'))

@bot.command()
async def ships():
    url = conf['url'].format("ships", "", "")
    response = urllib.request.urlopen(url).read()
    await bot.say("```" + str(response,'utf-8') + "```")

@bot.command(pass_context=True, no_pm=True)
@is_owner()
async def setnick(ctx, nick : str):
    me = ctx.message.server.me
    await bot.change_nickname(me, nick)
    await bot.say(":ok_hand:")

@bot.command()
@is_owner()
async def status(newgame : str):
    await bot.change_status(game=discord.Game(name=newgame))
    await bot.say(":ok_hand:")

@bot.command()
@is_owner()
async def shutdown():
    await bot.say(":wave:")
    await bot.logout()
    await bot.close()

if __name__ == "__main__":
    try:
        with open("config.json", "r") as f:
            conf = f.read()
        conf = json.loads(conf)
    except:
        print("config???")
        raise
        sys.exit()
    bot.run(conf["token"])