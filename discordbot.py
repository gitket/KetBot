import discord
import logging
import json
import subprocess
import os
import datetime
import requests
import re
import calendar
from string import punctuation
from bs4 import BeautifulSoup
import time
import numbers
from twitch import TwitchClient
from discord import Embed
from discord import Colour
from datetime import datetime, timedelta

#logger = logging.getLogger('discord')
#logger.setLevel(logging.INFO)
#handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
#handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
#logger.addHandler(handler)

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
    print('Logged in as', flush=True)
    print(client.user.name, flush=True)
    print('---------', flush=True)
    

@client.event
async def on_member_update(before, after):
    if before.server.id != serverid:
        return
    streamUrlBefore = getattr(before.game, "url", None)
    gameType = getattr(after.game, "type", 0)
    streamUrl = getattr(after.game, "url", None)
    if(streamUrl and gameType == 1):
        if(streamUrl == streamUrlBefore):
            print("dupe-skipping " + streamUrl, flush=True)
            return;
        print("looking at " + streamUrl, flush=True)
        print("before status " + str(before.status), flush=True)
        print("After status " + str(after.status), flush=True)
        print("total roles " + str(len(before.roles)), flush=True)
        if(len(before.roles) == 1):
            print("not a guildie-skipping", flush=True)
            return;
        channelName = after.game.url.split('/')[-1:]
        channel = twitch.search.channels(channelName)
        if channel:
            ch = channel[0]
            embed = Embed()
            embed.type = 'rich'
            if after.nick:
                embed.title = after.nick + ' now Streaming!'
            else:
                embed.title = after.display_name + 'Now Streaming!'
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
            uptime = get_uptime_min(ch.id)
            if(uptime > 2):
                print("uptime over 2 min, ignoring", flush=True)
                return;
            print(embed.to_dict(), flush=True)
            print(client.get_channel(streamChannel).name, flush=True)
            await client.send_message(client.get_channel(streamChannel), after.display_name + ' is now live! Watch the stream: '+ streamUrl,embed=embed)
            print("posted", flush=True)

def get_uptime_min(streamID):
    stream = twitch.streams.get_stream_by_user(streamID, 'live')
    created_at = stream.created_at
    createdSeconds = (created_at - datetime(1970, 1, 1)).total_seconds()
    nowUTC = (datetime.utcnow() - datetime(1970, 1, 1)).total_seconds()
    uptime = nowUTC - createdSeconds
    minute = uptime /60
    print("uptime is: " + str(minute), flush=True)
    return minute


client.run(token)
