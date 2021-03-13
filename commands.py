"""Defines bot commands"""

import os
import server

prefix = os.environ['MSB_PREFIX']

async def command_ping(msg):
    """Pings the bot (not the Minecraft server)"""

    await msg.reply('pong')

async def command_up(msg):
    """Checks if the Minecraft server is up"""

    if server.list_ping() is not None:
        await msg.reply(':white_check_mark: The server is up!')
    else:
        await msg.reply(':no_entry: The server is down.')

async def command_on(msg):
    """Prints how many players are on, and a sample of usernames (may not be all online players)"""

    if (j := server.list_ping()) is not None:
        if j['players']['online'] == 0:
            await msg.reply('Players: (0/'+str(j['players']['max'])+')')
        else:
            await msg.reply('Players ('+str(j['players']['online'])+
                '/'+str(j['players']['max'])+'): '+
                ', '.join([p['name'] for p in j['players']['sample']]))
    else:
        await msg.reply(':no_entry: The server is down.')

unprefixed = {
        'up': command_up,
        'on': command_on,
        'ping': command_ping
}

async def command_help(msg):
    """Uses docstrings to create a help message for each command"""

    content = ''
    for name in unprefixed:
        content += '`' + prefix + name + '` — ' + unprefixed[name].__doc__ + '\n'
    content += '\nThis bot is open source (MIT License), '
    content += 'contribute: <https://github.com/tteeoo/msb>'
    await msg.reply(content)

table = {prefix+'help': command_help}
for k in unprefixed:
    table[prefix+k] = unprefixed[k]
