#!/usr/bin/env python3

import os
import time
import server
import asyncio
import discord
import commands
import threading
from discord.ext import tasks

client = discord.Client()
interval = int(os.environ['MSB_INTERVAL'])
status = False
channel = None

@tasks.loop(seconds=interval)
async def uptime():
    global channel, status
    up = server.list_ping(False)
    if up and not status:
        status = True
        await channel.send(':white_check_mark: The server went up!') 
        await client.change_presence(status=discord.Status.online,
            activity=discord.Activity(type=discord.ActivityType.watching, name=server.host))
    elif not up and status:
        status = False
        await channel.send(':no_entry: The server went down.') 
        await client.change_presence(status=discord.Status.dnd,
            activity=discord.Activity(type=discord.ActivityType.watching, name=server.host))

@uptime.before_loop
async def before_uptime():
    global channel
    await client.wait_until_ready()
    channel = await client.fetch_channel(os.environ['MSB_CHANNEL'])

@client.event
async def on_ready():
    print('Ready -- Watching', server.host + ':' + str(server.port))

    if server.list_ping(False):
        await client.change_presence(status=discord.Status.online,
            activity=discord.Activity(type=discord.ActivityType.watching, name=server.host))
    else:
        await client.change_presence(status=discord.Status.dnd,
            activity=discord.Activity(type=discord.ActivityType.watching, name=server.host))

@client.event
async def on_message(msg):
    if msg.content in commands.table:
        await commands.table[msg.content](msg)

if __name__ == '__main__':
    if os.environ['MSB_CHANNEL'] != '': uptime.start()
    client.run(os.environ['MSB_TOKEN'])
