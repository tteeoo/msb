#!/usr/bin/env python3

import os
import server
import discord
import commands

client = discord.Client()

@client.event
async def on_ready():
    print("Ready!")
    await client.change_presence(status=discord.Status.online,
        activity=discord.Activity(type=discord.ActivityType.watching, name=server.host))

@client.event
async def on_message(msg):
    if msg.content in commands.table:
        await commands.table[msg.content](msg)

client.run(os.environ['MSB_TOKEN'])
