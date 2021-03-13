# Defines bot commands.

import os
import server

prefix = os.environ['MSB_PREFIX']

async def ping(msg):
    """Pings the bot (not the Minecraft server)"""

    await msg.reply('pong')

async def up(msg):
    """Checks if the Minecraft server is up"""

    if server.list_ping(False):
        await msg.reply(':white_check_mark: The server is up!')
    else:
        await msg.reply(':no_entry: The server is down.')

async def on(msg):
    """Prints how many players are on, and a sample of usernames (may not be all online players)"""

    if (j := server.list_ping(True)) != None:
        await msg.reply('Players ('+str(j['players']['online'])+'/'+str(j["players"]["max"])+'): '+ \
            ', '.join([p['name'] for p in j['players']['sample']]))
    else:
        await msg.reply(':no_entry: The server is down.')

unprefixed = {
        'up': up,
        'on': on,
        'ping': ping
}

async def help_(msg):
    content = ''
    for name in unprefixed:
        content += '`' + prefix + name + '` — ' + unprefixed[name].__doc__ + '\n'
    content += '\nThis bot is open source (MIT License), contribute: <https://github.com/tteeoo/msb>'
    await msg.reply(content)

table = {prefix+'help': help_}
for k in unprefixed:
    table[prefix+k] = unprefixed[k]
