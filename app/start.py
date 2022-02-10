import os
import discord

from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('API_KEY')

client = discord.Client()

@client.event
async def on_ready():
    print(client.user)


async def on_message(message):
    parseMsg(message)

def parseMsg(message):
    if message.content == command.exists:
        print(exists)

client.run(API_KEY)
