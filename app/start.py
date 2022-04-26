import os
import discord
import re
import sys
import time
import socket
import requests
import json
from scapy.all import *
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('API_KEY')
CHAT_LOG = os.getenv('CHAT_LOG')
RAPID_API_AVIATION_KEY = os.getenv('RAPID_API_AVIATION_KEY')
IP_GEOLOCATION_API = os.getenv('IP_GEOLOCATION_API')
botID = os.getenv('BOT_ID')
DISCORD_GUILD = os.getenv('DISCORD_GUILD')


client = discord.Client()
botChannel = "bot" + str(25)




# API

def searchAirport(message):
    ip = message.replace("fly me to","")
    url = "https://aviation-reference-data.p.rapidapi.com/airports/search"
    ip = validateIP(ip)
    results = IPToLocation(ip)
    latitude = str(results["latitude"])
    longitude = str(results["longitude"])
    radius = "100" # Miles around latlong
    querystring = {"lat":latitude,"lon":longitude,"radius":radius}
    print(querystring)
    headers = {
        'x-rapidapi-host': "aviation-reference-data.p.rapidapi.com",
        'x-rapidapi-key': RAPID_API_AVIATION_KEY,
        }
    response = requests.request("GET", url, headers=headers, params=querystring)
    print(headers)
    #print(response.text)
    data = json.loads(response.text)
    count = 0

    airportName = (data[count]["name"])
    airportCountry = (data[count]["alpha2countryCode"])

    print("IP: ",ip,"\nAIRPORT NAME: ",airportName,"\nCountry: ",airportCountry)

    results = ("NEAREST AIRPORT TO " + ip + " - " + airportName + " in " + airportCountry)
    return str(results)

# Discord bot events

@client.event
async def on_ready():
    print(client.user)

@client.event
async def on_message(message):

    if message.channel.name != botChannel: # Only replies to messages sent in botChannel
        return
    else:
        if message.author.bot:  # Bot doesn't reply to itself
            return
        else:
            logChat(message.author,message.content) # Log incoming message

            word = "onions" # wordReplace functionality
            if word in message.content:
                link = "cheese"
                await message.reply(wordReplace(word,link,message))

            elif "scan " in message.content: # Scapy init
                #if checkuserPermissions(str(message.author),"scan"):
                results = scan(message.content)
                await message.reply(results)
                #else:
                #    await message.reply("Permission denied")

            elif message.content == "help":
                await message.reply(help())

            elif message.content == "1":
                results = settings()
                await message.reply(settings())

            elif "fly me to " in message.content: # searchAirport init
                #if checkuserPermissions(str(message.author),"fly me to "):
                results = searchAirport(str(message.content))
                await message.reply(results)
                #else:
                #    await message.reply("Permission denied")

            else:
                await message.reply("Invalid Command")


# MENUS

def help(): # Help menu
    menu = "HELP MENU\n\n[1] Settings\n[2] Show Log\n[3] Delete Log"
    return menu

def settings(): # Bot settings menu
    menu = "SETTINGS MENU\n"
    return menu


# PORT SCANNER

# ICMP packet to validated IP or domain name
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


# FUN

def wordReplace(word,link,message):
    word = "green"
    if word in message.content:
        link = "cheese"
        text = message.content
        results = text.replace(word,link)
        return results
    else:
        return "Invalid word"


## UTILITY

# Validates IP with regex
def validateIP(ip):
    ipv4 = re.compile("^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$") # Loads ipv4 regex
    domain = re.compile("^((?!-))(xn--)?[a-z0-9][a-z0-9-_]{0,61}[a-z0-9]{0,1}\.(xn--)?([a-z0-9\-]{1,61}|[a-z0-9-]{1,30}\.[a-z]{2,})$") # Regex to match most domains
    isdomain = domain.match(ip)
    isipv4 = ipv4.match(ip) # Is users message valid ipv4 address
    try:
        if isipv4:
            return ip
        elif isdomain:
            print("IP",str(domaintoip(ip)))
            return str(domaintoip(ip))
        pass
    except Exception as e:
        pass

def domaintoip(ip):
    print("CHECKING", ip)
    return str(socket.gethostbyname(ip))

# Logs message to file
def logChat(user,message):
    data = str(user) + ": " + message
    print(data)
    with open(CHAT_LOG+".log", "a") as file:
        file.write(data+"\n")
        file.close()
        return True

# Get MaxMind latlong from ip

def IPToLocation(ip):
    url = "https://api.ipgeolocation.io/ipgeo?apiKey="+IP_GEOLOCATION_API+"&ip="+ip#+"&fields=city"
    response = requests.request("GET", url)
    data = response.text
    parsed = json.loads(data)
    results  = {
    "city":parsed["city"],
    "latitude":parsed["latitude"],
    "longitude":parsed["longitude"]
    }
    return results

## PERMISSIONS

# Checks user in elevated permissions list
def checkuserPermissions(user,action):
    print("Checking: " + user)
    with open("/users.list", "r") as file:
        lines = file.readlines()
        for line in lines:
            if str(user) in line:
                message = " executed " + action
                logChat(user,message)
                return True
        else:
            message = "DENIED EXECUTION: " + action
            logChat(user,message)
            return False
        file.close()

# Add user to elevated permissions list
def addPermissions(user):
    with open("users.list", "a") as file:
        file.write(user + "\n")
        file.close()


# INIT

def init():
    client.run(API_KEY)


init()
