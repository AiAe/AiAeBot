import discord
import json
import sys
import random
import pprint
from discord.ext import commands
import cleverbot
import time
import aiohttp
import MySQLdb
import io
import re
import asyncio
from PIL import Image
from time import gmtime, strftime

try:
    with open("./config.json", "r") as f: 
        conf = json.load(f)
except:
    print("config???")
    raise
    sys.exit()

description = ''' AiAeBot by Daniel '''
bot = commands.Bot(command_prefix='.', description=description)
bot.remove_command("help")
db = MySQLdb.connect(host=conf['host'], user=conf['user'], passwd=conf['passwd'], db=conf['db']) 
cursor  = db.cursor()

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
        return role_or_permissions(ctx, lambda r: r.name == conf['moderator_role'])

    return commands.check(predicate)

def roleCheck(self, server, name):
    Roles = server.roles
    for Role in Roles[:]:
        if Role.name == name:
            return True
        else:
            pass
    return False

async def shiping():
    await bot.wait_until_ready()
    while not bot.is_closed:
        atmhour = strftime("%I:%M", gmtime())
        if atmhour in conf['ship_time']:
            cursor.execute("SELECT * FROM ships ORDER BY RAND() LIMIT 1")
            row = cursor.fetchone()
            cursor.execute("UPDATE ships SET counter='%s' WHERE id='%s'", [(row[3]+1), row[0]])
            db.commit()
            await bot.send_message(discord.Object(id="203956255197364224"), "{} x {}".format(row[1], row[2]))
        await asyncio.sleep(int(conf['ship_checker_time']))

@bot.event
async def on_ready():
    await bot.change_presence(game=discord.Game(name=conf['default_game']))

@bot.async_event
async def on_member_join(member):
    server = member.server
    await bot.send_message(server, "Welcome to " + server.name + " " + member.mention + "!")

@bot.async_event
async def on_member_remove(member):
    server = member.server
    await bot.send_message(server, member.mention + " left us :frowning2:")

@bot.command()
@admin_or_permissions()
async def addship(username1 : str, username2 : str):
    cursor.execute("SELECT * FROM ships WHERE username_1='%s' and username_2='%s'", [username1, username2])
    counter = cursor.rowcount
    if counter == 1:
        await bot.say("Ship exists in database!", delete_after=5)
    else: 
        cursor.execute("SELECT * FROM ships WHERE username_1='%s' and username_2='%s'", [username2, username1])
        counter2 = cursor.rowcount
        if counter2 == 1:
            await bot.say("Ship exists in database!", delete_after=5)
        else:
            cursor.execute("INSERT INTO ships (username_1, username_2) VALUES('%s', '%s')", [username1, username2])
            db.commit()
            await bot.say("Added.", delete_after=5)

@bot.command()
@admin_or_permissions()
async def rship(ship1 : str, ship2 : str):
    cursor.execute("DELETE FROM ships WHERE username_1='%s' and username_2='%s'", [username1, username2])
    db.commit()
    await bot.say("Ship is removed.", delete_after=5)

@bot.command()
async def ships():
    cursor.execute("SELECT  * FROM ships")
    results = cursor.fetchall()
    usernames = []
    for row in results:
        usernames.append("{} x {} Counter: {}\n".format(re.sub(r"[^A-Za-z]+", '', row[1]), re.sub(r"[^A-Za-z]+", '', row[2]), row[3]))
    s = ''.join(map(str, usernames))
    await bot.whisper("```{}```".format(s))

@bot.command(pass_context=True, no_pm=True)
@commands.cooldown(1, 30, commands.BucketType.user)
async def getavatar(ctx, member : discord.Member = None):
    await bot.say(member.avatar_url)

@bot.command(pass_context=True, no_pm=True)
@commands.cooldown(1, 60, commands.BucketType.user)
async def mf(ctx, fname : str):
    i = 0
    count = len(conf['mf'])
    while True:
        if i is count:
            await bot.say("Middle Finger not found.")
            break
        else:
            if fname in conf['mf'][i].split(".")[0]:
                await bot.send_file(ctx.message.channel, './fingers/{}'.format(conf['mf'][i]))
                break
            else:
                i += 1
            
@bot.command(name="8ball")
@commands.cooldown(1, 10, commands.BucketType.user)
async def eight_ball(*text):
    await bot.say(random.choice(conf['answers']))

@bot.command(pass_context=True)
@commands.cooldown(1, 10, commands.BucketType.user)
async def kys(ctx, message, *text):
    cleverbot_client = cleverbot.Cleverbot()
    answer = cleverbot_client.ask(str(text))
    await bot.say(answer)

@bot.command(pass_context=True, no_pm=True)
@is_owner()
async def setnick(ctx, nick : str):
    me = ctx.message.server.me
    await bot.change_nickname(me, nick)
    await bot.say(":ok_hand:")

@bot.command(pass_context=True, no_pm=True)
@is_owner()
async def setavatar(ctx, message):
    url = message
    imgType = url.split('.')[-1]
    request = await aiohttp.request('get', url)
    raw = await request.read()
    imageData = bytes(raw)
    pngImage = Image.open(io.BytesIO(imageData))
    pngImage.save("avatar_temp.png")
    avatarImage = open("avatar_temp.png", "rb")
    await bot.edit_profile(avatar=avatarImage.read())
    avatarImage.close()
    await bot.send_message(ctx.message.channel, ":ok_hand:")

@bot.command(no_pm=True)
@admin_or_permissions()
async def mute(user: discord.Member, *, reason: str="for no reason"):
    server = user.server
    role = discord.utils.get(user.server.roles, name=conf['mute_role'])
    await bot.add_roles(user, role)
    await bot.say(conf['default_mute_msg'].format(user, reason))

@bot.command(no_pm=True)
@admin_or_permissions()
async def unmute(user: discord.Member):
    server = user.server
    role = discord.utils.get(user.server.roles, name=conf['mute_role'])
    await bot.remove_roles(user, role)
    await bot.say(conf['default_unmute_msg'].format(user))

@bot.command(no_pm=True)
@admin_or_permissions()
async def addrole(user: discord.Member, r : str):
    server = user.server
    if r in conf['roles']:
        role = discord.utils.get(user.server.roles, name=r)
        await bot.add_roles(user, role)
        await bot.say(":ok_hand:", delete_after=5)
    else: 
        return await bot.say(":middle_finger:", delete_after=5)

@bot.command(pass_context=True, no_pm=True)
@admin_or_permissions()
async def purge(ctx, name : str, amount : int=10):
    # Not my code. I will put source if I don't forget
    try:
        found = discord.utils.find(lambda m: name.lower() in m.display_name.lower(), ctx.message.server.members)
    except:
        found = None

    if found is None:
        found = discord.utils.find(lambda m: name == m.mention, ctx.message.server.members)

    if found is None:
        await bot.say("{} not found".format(name))
        return

    if not ctx.message.server.me.permissions_in(ctx.message.channel).manage_messages:
        return

    delete_list = []
    async for msg in bot.logs_from(ctx.message.channel, limit=(amount*5)):
            if len(delete_list) == amount:
                break
            if msg.author.id == found.id:
                delete_list.append(msg)

    if len(delete_list) == 1:
        await bot.delete_message(delete_list[0])
    elif len(delete_list) >= 2:
        for i in range(len(delete_list)//100 + 1):
            await bot.delete_messages(delete_list[100*i:100*(i+1)])
            await asyncio.sleep(0.5)

@bot.command()
@is_owner()
async def status(newgame : str):
    await bot.change_status(game=discord.Game(name=newgame))
    await bot.say(":ok_hand:", delete_after=5)

@bot.command()
async def help():
    await bot.whisper("```{}```".format(conf['help']))

@bot.command()
@is_owner()
async def shutdown():
    await bot.say(":wave:")
    await bot.logout()
    await bot.close()

if __name__ == "__main__":
    bot.loop.create_task(shiping())
    bot.run(conf["token"])