# Discord Bot - README.md

### DISCLAIMER: THIS IS FOR EDUCATIONAL USE ONLY. I TAKE NO RESPONSIBILITY FOR MISUSE OF SCAPY AND/OR OTHER FUNCTIONALITY BUILT INTO THIS PROGRAM.

This document plans to cover the funcitonality of the discord bot in as much detail as possible.

[SKIP TO SETUP](https://github.com/elliottmotson/discord-bot/blob/documentation-phase-1/README.md#setup)

---

# Features

- OPENAI Davinci-002 functionality
- Scapy ICMP packet crafting for valid IPs and TLDs
- Domain & IP validation for commands
- IP to Geolocation
- Local user account permissions list
- Local chat logging
- Word swap
- Help menu
- Settings menu

## Networking

- Scan %IP OR VALID TLD% // Crafts ICMP packet through Scapy and prints outcome as OFFLINE or ONLINE

---

# OPENAI

## Commands

- Call openai using "." operator to feed davinci data - Example command:
1. .Tell me a story
2. .Shall I fly via Paris or London?
3. .Open the pod bay doors, HAL
- openai setkey $KEY$ // Sets openai key
- openai showkey      // Displays current openai key
- openai disable      // Disables openai functionality



# IP GEOLOCATION

## Commands

- ipgeo setkey $KEY$ // Sets ipgeo key
- ipgeo showkey      // Displays current ipgeo key
- ipgeo disable      // Disables ipgeo functionality



# RAPIDAPI FLIGHT DATA API

## Commands

- fly me to %IP OR VALID TLD% // Uses combination of ipgeo & flight api to fetch closest airport to IP address⋅⋅⋅
- rapidapi setkey $KEY$ // Sets rapidapi key
- rapidapi showkey      // Displays current rapidapi key
- rapidapi disable      // Disables rapidapi functionality


--- 


# Setup

Create a virtual environment
```python3 -m venv venv```

Install dependencies
```pip install -r requirements.txt```

Copy .env file - Remember to set your API keys!
```cp .env.example .env``` 

Start the application (May need sudo due to scapy)
```python3 ./app/start.py```


