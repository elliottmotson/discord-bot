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
from pathlib import Path

# Environment vars

load_dotenv()
API_KEY = os.getenv('API_KEY')
CHAT_LOG = os.getenv('CHAT_LOG')
BOT_ID = os.getenv('BOT_ID')
DISCORD_GUILD = os.getenv('DISCORD_GUILD')

# API Keys

IP_GEOLOCATION_API_KEY = os.getenv('IP_GEOLOCATION_API_KEY')
RAPID_API_AVIATION_KEY = os.getenv('RAPID_API_AVIATION_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY

# Discord object vars

client = discord.Client()
botChannel = "bot" + str(BOT_ID)

## API functionality

# OpenAI text processing

def ai(text):
    response = openai.Completion.create( # Crafts API response for davinci OpenAI
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


# RAPIDAPI Aviation call


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

        ## Main keyword triggers ##

        # Word Replace

            logChat(message.author,message.content) # Log incoming message
            word = "onions" # wordReplace keyword
            if word in message.content:
                link = "cheese"
                await message.reply(wordReplace(word,link,message))

        # Scapy

            elif "scan " in message.content: # Scapy init
                if checkuserPermissions(message,"scan"):
                    results = scan(message.content)
                    await message.reply(results)
                else:
                    await message.reply("Permission denied")

        # Menu call

            elif message.content == "help":
                await message.reply(help())

            elif message.content == "1": # Load settings [1]
                await settings(message)

            elif message.content == "2": # Show log [2]
            # Read log file, return as discord messages
                data = []
                if checkuserPermissions(message, "View log"):
                    path = Path(f"./{CHAT_LOG}.log")
                    if path.is_file():
                        with open(f"./{CHAT_LOG}.log", "r") as file:
                            lines = file.readlines()
                            await message.reply(f"PRINTING {CHAT_LOG.upper()} HISTORY")
                            for line in lines:
                                data.append(line.strip()+"\n")
                                result = "".join(data)
                                print(result)
                            await message.reply(result)


            elif message.content == "3": # Delete log [3]
                if checkuserPermissions(message, "Delete log"):
                    print(f"{str(message.author)} deleting file")
                    logfile = CHAT_LOG+".log"
                    os.remove(logfile) # If logfile exists, delete
                    gencoreFiles()
                    await message.reply(f"{logfile} deleted by {message.author}. Regenerated blank core files")

        # Airport search call

            elif "fly me to " in message.content: # searchAirport init
                if checkuserPermissions(message,"fly me to "):
                    results = searchAirport(message.content)
                    await message.reply(results)

# API calls

        # OPENAI
        # Call openai using . operator - Example command: .Tell me a story
        # openai setkey %KEY% // Sets openai key
        # openai showkey // Displays current openai key
        # openai disable // Disables openai functionality

            elif "openai setkey " in message.content:
                if checkuserPermissions(message,"openai setkey"):
                    message.content.replace("openai setkey","")
                    OPENAI_API_KEY = message.content
                    await message.reply(f"OPENAI KEY CHANGE TO: {os.getenv('OPENAI_API_KEY')}")
            elif "openai showkey" in message.content:
                if checkuserPermissions(message,"openai showkey"):
                    await message.reply(f"OPENAI KEY: {os.getenv('OPENAI_API_KEY')}")
            elif "openai disable" in message.content:
                if checkuserPermissions(message,"openai disable"):
                    await message.reply("OPENAI DISABLED - FEATURE TO BE COMPLETED")
            elif message.content.startswith("."):
                await message.reply(ai(message.content))


        # IP GEOLOCATION
        # ipgeo setkey %KEY% // Sets ipgeo key
        # ipgeo showkey // Displays current ipgeo key
        # ipgeo disable // Disables ipgeo functionality


            elif "ipgeo setkey " in message.content:
                if checkuserPermissions(message,"ipgeo setkey"):
                    message.content.replace("ipgeo setkey","")
                    IP_GEOLOCATION_API_KEY = message.content
                    await message.reply(f"IPGEO KEY CHANGE TO: {os.getenv('IP_GEOLOCATION_API_KEY')}")
            elif "ipgeo showkey" in message.content:
                if checkuserPermissions(message,"ipgeo showkey"):
                    await message.reply(f"IPGEO KEY: {os.getenv('IP_GEOLOCATION_API_KEY')}")
            elif "ipgeo disable" in message.content:
                if checkuserPermissions(message,"ipgeo disable"):
                    await message.reply("IPGEO DISABLED - FEATURE TO BE COMPLETED")


        # RAPID API
        # rapidapi setkey %KEY% // Sets rapidapi key
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
            elif message.content == "isadmin":
                if checkuserPermissions(message,"isadmin"):
                    await message.reply(f"{message.author} is admin")
                else:
                    await message.reply(f"{message.author} is NOT admin")
            else:
                await message.reply("Invalid Command") # If user input doesn't match anything in on_message()


## MENUS

# Help

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


## PORT SCANNER

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
    ipv4 = re.compile("^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$") # Loads ipv4 regex validation string
    domain = re.compile("^((?!-))(xn--)?[a-z0-9][a-z0-9-_]{0,61}[a-z0-9]{0,1}\.(xn--)?([a-z0-9\-]{1,61}|[a-z0-9-]{1,30}\.[a-z]{2,})$") # Regex to match most TLDs
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
    url = "https://api.ipgeolocation.io/ipgeo?apiKey="+IP_GEOLOCATION_API_KEY+"&ip="+ip # IP GEOLOCATION
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
def checkuserPermissions(message,action):
    user = str(message.author).strip()
    print(f"Checking: {user}")
    path = Path("./users.list")
    if path.is_file():
        with open("./users.list", "r") as file:
            lines = file.readlines()
            for line in lines:
                if user in line:
                    message = f"{user} executed {action}"
                    #logChat(message.author,message)
                    file.close()
                    return True
    else:
        message = "DENIED EXECUTION: " + action
        logChat(message.author,message)
        file.close()
        return False

# Add user to elevated permissions list
def addPermissions(user):
    with open("./users.list", "a") as file:
        file.write(user + "\n")
        file.close()
        print(f"Added {user} to ./users.list")


## INIT

def gencoreFiles():
    # If path exists
    # return True
    # else generate gencoreFiles
    # ./chat.log
    # ./users.list
    userspath = Path("./users.list")
    print(f"Checking if {userspath} exists")

    if userspath.is_file(): # If user admin file exists
        print(f"{userspath} exists")

    else:
        print(f"Generating {str(userspath)}")
        with open(userspath, "a") as file:
            file.write("")
            file.close()
            print(f"{str(userspath)} generated")

    chatpath = Path(f"./{CHAT_LOG}.log")
    print(f"Checking if {CHAT_LOG}.log exists")
    if chatpath.is_file(): # If chat log file exists
        print(f"{CHAT_LOG}.log exists")
    else:
        print(f"Generating {str(chatpath)}")
        with open(chatpath, "a") as file:
            file.write("")
            file.close()
            print(f"{str(chatpath)} generated")


def init(): # Init/main function

    #Generates core files if not exist
    gencoreFiles()
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
        init()
        return False


init()
