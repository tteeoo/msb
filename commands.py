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

async def command_server(msg):
    """Prints information about the server being monitored"""

    if (j := server.list_ping()) is not None:
        content = '**Server:** ' + server.host + ':' + str(server.port) + '\n'
        if 'description' in j and 'text' in j['description']:
            content += '**Description:** ' + j['description']['text'] + '\n'
        if 'version' in j and 'name' in j['version']:
            content += '**Version:** ' + j['version']['name'] + '\n'
        if 'modinfo' in j:
            content += '**Mods:** ' + (str(len(j['modinfo']['modList'])) if 'modList' in j['modinfo'] else 'Yes') + '\n'
        else:
            content += '**Mods:** No'
        await msg.reply(content)
    else:
        await msg.reply(':no_entry: The server is down.')

async def command_mods(msg):
    """Prints information about the mods on the server"""

    if (j := server.list_ping()) is not None:
        content = ''
        if 'modinfo' in j:
            if 'modList' in j['modinfo']:
                content += '\n'.join(
                    [m['modid'] + ' version ' + m['version'] for m in j['modinfo']['modList']]
                )
            else:
                content += 'Could not get mod info.'
        else:
            content += 'No mods on the server.'
        await msg.reply(content)
    else:
        await msg.reply(':no_entry: The server is down.')

unprefixed = {
        'up': command_up,
        'on': command_on,
        'ping': command_ping,
        'server': command_server,
        'mods': command_mods
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
