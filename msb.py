#!/usr/bin/env python3

import os
import discord
from discord.ext import tasks
import server
import commands

client = discord.Client()
interval = int(os.environ['MSB_INTERVAL'])

class Uptime:
    """Controls the uptime detection/announcement system"""

    def __init__(self, client):
        self.client = client
        self.status = False
        self.channel = None

    @tasks.loop(seconds=interval)
    async def uptime(self):
        up = server.list_ping()
        if up is not None and not self.status:
            self.status = True
            await self.channel.send(':white_check_mark: The server went up!')
            await client.change_presence(status=discord.Status.online,
                activity=discord.Activity(type=discord.ActivityType.watching, name=server.host))
        elif up is None and self.status:
            self.status = False
            await self.channel.send(':no_entry: The server went down.')
            await self.client.change_presence(status=discord.Status.dnd,
                activity=discord.Activity(type=discord.ActivityType.watching, name=server.host))

    @uptime.before_loop
    async def before_uptime(self):
        await client.wait_until_ready()
        self.channel = await client.fetch_channel(os.environ['MSB_CHANNEL'])

@client.event
async def on_ready():
    print('Ready -- Watching', server.host + ':' + str(server.port))
    if server.list_ping() is not None:
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
    if os.environ['MSB_CHANNEL'] != '': Uptime(client).uptime.start()
    client.run(os.environ['MSB_TOKEN'])
