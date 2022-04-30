import os
import discord
import re
import sys
import time
import socket
import requests
import json
import openai
from scapy.all import *
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('API_KEY')
CHAT_LOG = os.getenv('CHAT_LOG')
BOT_ID = os.getenv('BOT_ID')
DISCORD_GUILD = os.getenv('DISCORD_GUILD')

IP_GEOLOCATION_API_KEY = os.getenv('IP_GEOLOCATION_API_KEY')
RAPID_API_AVIATION_KEY = os.getenv('RAPID_API_AVIATION_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY


client = discord.Client()
botChannel = "bot" + str(BOT_ID)

def ai(text):
    response = openai.Completion.create(
    engine="text-davinci-002",
    prompt=text,
    temperature=0.4,
    max_tokens=60,
    top_p=1,
    frequency_penalty=0.5,
    presence_penalty=0,
    stop=["You:"]
    )
    print(response)
    content = response.choices[0]
    content = content.text.replace("?","")
    content = content.strip()
    print(content)
    return content


# API

def searchAirport(message):
    ip = message.replace("fly me to ","")
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
                if checkuserPermissions(str(message.author),"scan"):
                    results = scan(message.content)
                    await message.reply(results)
                else:
                    await message.reply("Permission denied")

            elif message.content == "help":
                await message.reply(help())

            elif message.content == "1":
                await settings(message)

            elif "fly me to " in message.content: # searchAirport init
#                if checkuserPermissions(str(message.author),"fly me to "):
                results = searchAirport(message.content)
                await message.reply(results)
#            else:
#                await message.reply("Permission denied")

        # OPENAI
        # Call openai using . operator - Example command: .Tell me a story
        # openai setkey $KEY$ // Sets openai key
        # openai showkey // Displays current openai key
        # openai disable // Disables openai functionality

            elif message.content in "openai setkey ":
                message.content.replace("openai setkey","")
                OPENAI_API_KEY = message.content
                await message.reply(f"OPENAI KEY CHANGE TO: {os.getenv('OPENAI_API_KEY')}")
            elif message.content in "openai showkey":
                await message.reply(f"OPENAI KEY: {os.getenv('OPENAI_API_KEY')}")
            elif message.content in "openai disable":
                await message.reply("OPENAI DISABLED - FEATURE TO BE COMPLETED")
            elif message.content.startswith("."):
                await message.reply(ai(message.content))


        # IP GEOLOCATION
        # ipgeo setkey $KEY$ // Sets ipgeo key
        # ipgeo showkey // Displays current ipgeo key
        # ipgeo disable // Disables ipgeo functionality


            elif message.content in "ipgeo setkey ":
                message.content.replace("ipgeo setkey","")
                IP_GEOLOCATION_API_KEY = message.content
                await message.reply(f"IPGEO KEY CHANGE TO: {os.getenv('IP_GEOLOCATION_API_KEY')}")
            elif message.content in "ipgeo showkey":
                await message.reply(f"IPGEO KEY: {os.getenv('IP_GEOLOCATION_API_KEY')}")
            elif message.content in "IPGEO disable":
                await message.reply("IPGEO DISABLED - FEATURE TO BE COMPLETED")


        # RAPID API
        # rapidapi setkey $KEY$ // Sets rapidapi key
        # rapidapi showkey // Displays current rapidapi key
        # rapidapi disable // Disables openai functionality


            elif message.content in "rapidapi setkey ":
                message.content.replace("rapidapi setkey","")
                RAPID_API_AVIATION_KEY = message.content
                await message.reply(f"RAPIDAPI KEY CHANGE TO: {os.getenv('RAPID_API_AVIATION_KEY')}")
            elif message.content in "rapidapi showkey":
                await message.reply(f"RAPIDAPI KEY: {os.getenv('RAPID_API_AVIATION_KEY')}")
            elif message.content in "rapidapi disable":
                await message.reply("RAPIDAPI DISABLED - FEATURE TO BE COMPLETED")
            else:
                await message.reply("Invalid Command")


# MENUS

def help(): # Help menu
    menu = "HELP MENU\n\n[1] Settings\n[2] Show Log\n[3] Delete Log"
    return menu


# Settings Menu

async def settings(message): # Bot settings menu
    await message.reply("* SETTINGS *")
    await message.reply("# OPENAI\n# openai setkey $KEY$ // Sets openai key\n# openai showkey // Displays current openai key\n# openai disable // Disables openai functionality"
)
    await message.reply("# IP GEOLOCATION\n# ipgeo setkey $KEY$ // Sets ipgeo key\n# ipgeo showkey // Displays current ipgeo key\n# ipgeo disable // Disables ipgeo functionality"
)
    await message.reply("# RAPID API\n# rapidapi setkey $KEY$ // Sets rapidapi key\n# rapidapi showkey // Displays current rapidapi key\n# rapidapi disable // Disables openai functionality"
)


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
    url = "https://api.ipgeolocation.io/ipgeo?apiKey="+IP_GEOLOCATION_API_KEY+"&ip="+ip#+"&fields=city"
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
    with open("./users.list", "r") as file:
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
    if client.run(API_KEY):
        print("Connection established")
        return True
    else:
        print("Connection unavailable or API key invalid...")
        print("Retrying in 3")
        time.sleep(1)
        print("Retrying in 2")
        time.sleep(1)
        print("Retrying in 1")
        time.sleep(1)
        return False

init()
