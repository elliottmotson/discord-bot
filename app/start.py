import os
import discord
import re
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('API_KEY')

client = discord.Client()

@client.event
async def on_ready():
    print(client.user)

@client.event
async def on_message(message):
    if message.author.bot:
        return
    if "scan " in message.content:
        results = scan(message.content)
        await message.reply(results)

    elif message.content == "help":
        await message.reply(help())

    elif message.content == "1":
        results = settings()
        await message.reply(settings())
    else:
        await message.reply("Invalid Command")

#MENUS

def help():
    menu = "HELP MENU\n\n[1] Settings\n[2] Show Log\n[3] Delete Log"
    return menu

def settings():
    menu = "SETTINGS MENU\n"
    return menu

# PORT SCANNER

def scan(message):
    message = message.strip("scan ")
    ipv4 = re.compile("^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$") # Loads ipv4 regex
    isipv4 = ipv4.match(message) # Is users message valid ipv4 address
    if isipv4:
        print("Scanning address -",message)
        results = "OUTPUT OF SCAN"
        return results
    else:
        print("Not IP address")



client.run(API_KEY)
