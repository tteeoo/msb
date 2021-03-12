#!/usr/bin/env python3

import os
import discord
import commands

client = discord.Client()

@client.event
async def on_message(msg):
    if msg.content in commands.table:
        await commands.table[msg.content](msg)

client.run(os.environ['MSB_TOKEN'])
