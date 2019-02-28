import discord
import json
import subprocess
import os
import datetime
import requests
import re
from string import punctuation
from bs4 import BeautifulSoup
import time
import numbers

client = discord.Client()
with open('config.json') as config_data:
    config_json = json.load(config_data)
    api_key = config_json['api_key']
    token = config_json['discord_token']
    channel = config_json['channel'];
    serverid = config_json['serverid'];

@client.event
async def on_ready():
#On ready, joins all servers in JSON
    for x in config_json['servers']:
        client.accept_invite(x)
    print('Logged in as')
    print(client.user.name)
    print('---------')
    

@client.event
async def on_member_update(before, after):
    if before.server.id != serverid:
        return
    gameType = getattr(after.game, "type", 0)
    streamUrl = getattr(after.game, "url", None)
    if streamUrl:
        print(after.game.url)

client.run(token)
