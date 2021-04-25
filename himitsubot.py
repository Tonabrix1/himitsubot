import os
import discord
from discord.ext import commands
import time
import random


token = os.environ['token']
client = discord.Client()
bot = commands.Bot('!')

cmd = {
    'pneuma': lambda x: pneuma(x),
    'clear': lambda x: clear(x),
    'searchdex': lambda x: search(x),
    'searchutil': lambda x: searchutil(x),
    'searchdeep': lambda x: searchdeep(x),
    **dict.fromkeys(['info','commands'],lambda x: info(x)),
    'penis' : lambda x: penis(x)
}

def initiate(): 
    client.run(token)

@client.event
async def on_ready(): print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(msg):
    if msg.content[0] == bot.command_prefix: 
        #try:
            await process_commands(msg)
        #except:
         #   await msg.channel.send("either not a valid command or the code ran into an error")

async def process_commands(msg):
    global cmd
    func = cmd.get(str(msg.content.split(" ")[0][1:]).lower())
    await func(msg)

async def pneuma(msg):
    dex_guild = client.get_guild(682346582389030938)
    for channel in dex_guild.text_channels:
        if msg.content.split(" ")[1].lower() in channel.name:
            print("found match")
            async for message in channel.history(limit=200):
                if len(message.attachments) > 0:
                    for pic in message.attachments:
                        await msg.channel.send(pic.proxy_url)
                        time.sleep(1)
                if len(message.content) > 1: 
                    await msg.channel.send(message.content)
                    time.sleep(1)
            return

async def clear(msg):
    num = msg.content.split(" ")[1]
    if num != 'all':
        number = int(num) + 1  # Converting the amount of messages to delete to an integer
        counter = 0
        async for x in msg.channel.history(limit=number):
            if await check_halt(msg): return
            if counter < number:
                await x.delete()
                counter += 1
                time.sleep(1)
    else:
        async for x in msg.channel.history():
            if await check_halt(msg): return
            await x.delete()
            time.sleep(1)

async def search(msg):
    dex_guild = client.get_guild(682346582389030938)
    for cat in dex_guild.categories:
        if 'pneuma' not in cat.name.lower(): continue
        for channel in cat.text_channels:
            mes = msg.content.split(" ")[1].lower()
            if mes in channel.name[:len(mes)]:
                await msg.channel.send("<#" + str(channel.id) + ">")

async def searchutil(msg):
    dex_guild = client.get_guild(682346582389030938)
    for cat in dex_guild.categories:
        if 'pneuma' in cat.name.lower(): continue
        if 'demo' in cat.name.lower(): continue
        for channel in cat.text_channels:
            mes = msg.content.split(" ")[1].lower()
            if mes in channel.name:
                await msg.channel.send("<#" + str(channel.id) + ">")
                time.sleep(1)

async def searchdeep(msg):
    dex_guild = msg.guild
    for cat in dex_guild.categories:
        if 'pneuma' in cat.name.lower(): continue
        if 'demo' in cat.name.lower(): continue
        for channel in cat.text_channels:
            mes = str([a + " " for a in msg.content.split(" ")[1:]]).lower()
            async for m in channel.history(limit=200):
                if mes in m.content.lower():
                    await msg.channel.send("<#" + str(channel.id) + ">")
                    break
                    time.sleep(1)
    await msg.channel.send("All messages searched.")
         
async def info(msg):
    global cmd
    for key in cmd:
        await msg.channel.send(key)
        time.sleep(1)

async def check_halt(msg):
    if msg.content.split(" ")[0] in ['stop','halt','quit','exit','cancel']: return True
    return False

async def penis(msg):
    await msg.channel.send("8"+"="*random.randint(0,20)+"D")
    
initiate()
