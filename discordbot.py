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
from twitch import TwitchClient
from discord import Embed
from discord import Colour

client = discord.Client()
with open('config.json') as config_data:
    config_json = json.load(config_data)
    api_key = config_json['api_key']
    twitch_api_key = config_json['twitch_api_key']
    twitch_client_id = config_json['twitch_api_client_id']
    token = config_json['discord_token']
    streamChannel = config_json['channel'];
    serverid = config_json['serverid'];
    twitch = TwitchClient(client_id=twitch_client_id)

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
    streamUrlBefore = getattr(before.game, "url", None)
    gameType = getattr(after.game, "type", 0)
    streamUrl = getattr(after.game, "url", None)
    if(streamUrl and gameType == 1):
        if(streamUrl == streamUrlBefore):
            print("dupe-skipping " + streamUrl)
            return;
        print("looking at " + streamUrl)
        channelName = after.game.url.split('/')[-1:]
        channel = twitch.search.channels(channelName)
        if channel:
            ch = channel[0]
            embed = Embed()
            embed.type = 'rich'
            embed.title = after.nick + ' now Streaming!'
            embed.url = after.game.url
            embed.colour = discord.Colour(0x5441a5)
            embed.set_footer(text='Created by CromBot')
            if ch.game:
                embed.add_field(name='Now Playing', value=ch.game)
            embed.add_field(name='Stream Title', value=ch.status)
            embed.add_field(name='Followers', value=ch.followers)
            embed.add_field(name='Views', value=ch.views)
            if ch.profile_banner:
                embed.set_image(url=ch.profile_banner)
            print(embed.to_dict())
            print(client.get_channel(streamChannel).name)
            await client.send_message(client.get_channel(streamChannel), after.nick + ' is now live! Watch the stream: '+ streamUrl,embed=embed)
            print("posted")

while True:
	try:
		client.loop.run_until_complete(client.start(token))
	except BaseException:
			time.sleep(5)
