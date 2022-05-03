# Discord Bot - README.md

This document plans to cover the funcitonality of the discord bot in as much detail as possible.

### DISCLAIMER: THIS IS FOR EDUCATIONAL USE ONLY. I TAKE NO RESPONSIBILITY FOR MISUSE OF SCAPY AND/OR OTHER FUNCTIONALITY BUILT INTO THIS PROGRAM.

---

# Features

- OPENAI Davinci-002 functionality
- Scapy ICMP packet crafting for valid IPs and TLDs
- 

## Networking

- Scan %IP OR VALID TLD%
⋅⋅⋅ Crafts ICMP packet through Scapy and prints outcome as OFFLINE or ONLINE

##

# OPENAI

## Commands

- Call openai using "." operator to feed davinci data - Example command: 
⋅⋅⋅ .Tell me a story
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

- fly me to %IP OR VALID TLD%
⋅⋅⋅ Uses combination of ipgeo & flight api to fetch closest airport to IP address
- rapidapi setkey $KEY$ // Sets rapidapi key
- rapidapi showkey      // Displays current rapidapi key
- rapidapi disable      // Disables rapidapi functionality
