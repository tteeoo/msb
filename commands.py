# Defines bot commands.

import server

async def ping(msg):
    await msg.reply('pong')

async def up(msg):
    if server.list_ping(False):
        await msg.reply(':white_check_mark: The server is up!')
    else:
        await msg.reply(':no_entry: The server is down.')

async def on(msg):
    if (j := server.list_ping(True)) != None:
        await msg.reply(f'Players ('+str(j['players']['online'])+'/'+str(j["players"]["max"])+'): '+ \
            ', '.join([p['name'] for p in j['players']['sample']]))
    else:
        await msg.reply(':no_entry: The server is down.')

unprefixed = {
        'up': up,
        'on': on,
        'ping': ping
}

prefix = '!'
table = {}
for k in unprefixed:
    table[prefix+k] = unprefixed[k]
