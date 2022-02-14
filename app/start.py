import os
import discord
import re
import sys
import time
from scapy.all import *
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('API_KEY')
CHAT_LOG = os.getenv('CHAT_LOG')
client = discord.Client()

# Discord bot events

@client.event
async def on_ready():
    print(client.user)

@client.event
async def on_message(message):
    if message.author.bot:
        return
    else:
        logChat(message.author,message.content)

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

# MENUS

def help():
    menu = "HELP MENU\n\n[1] Settings\n[2] Show Log\n[3] Delete Log"
    return menu

def settings():
    menu = "SETTINGS MENU\n"
    return menu

# PORT SCANNER

def scan(message):
    message = message.strip("scan ")
    if validateIP(message):
        print("Scanning address -",message)
        ans, unans = sr(IP(dst=message)/ICMP(),timeout = 2)
        if ans:
            results = message+" - Online"
            print(str(ans))
            return results
        else:
            results = message+" - Offline"
            return results
    else:
        results = "Invalid IP or Domain"
        return results

# UTILITY

def validateIP(ip):
    ipv4 = re.compile("^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$") # Loads ipv4 regex
    isipv4 = ipv4.match(ip) # Is users message valid ipv4 address
    try:
        if isipv4:
            return ip
        else:
            return ip
        pass
    except Exception as e:
        pass

def logChat(user,message):
    data = str(user) + ": " + message
    print(data)
    with open(CHAT_LOG+".log", "a") as file:
        file.write(data+"\n")
        file.close()
        return True

def checkuserPermissions(user):
    with open("users.log", "r") as file:
        lines = file.readlines()
        for line in lines:
            if line == user:
                return True

# INIT

def addPermissions(user):
    with open(CHAT_LOG+".log", "a") as file:
        file.write(user + "\n")
        file.close()


client.run(API_KEY)
