# A Minecraft Server Bot (for Discord)

This is a Discord bot designed to provide information about a Minecraft server in Discord.

It can ping a Minecraft server at intervals and note its uptime in a specified channel.

## Commands

* `!up` — Checks if the Minecraft server is up.
* `!on` — Prints how many players are on, and a sample of usernames (may not be all online players).
* `!ping` — Pings the bot (not the Minecraft server).
* `!server` — Prints information about the server being monitored.
* `!mods` — Prints information about the mods on the server.

The prefix (default is exclamation point) can be changed.

## Running

This bot runs with Python versions >= 3.8.

Clone this repository and install the requirements:
```sh
$ git clone https://github.com/tteeoo/msb
$ cd msb/
$ python3 -m pip install -r requirements.txt
```

Create `.env`:
```sh
export MSB_TOKEN="" # From Discord developer pannel
export MSB_HOST="" # IP address or domain name of MC server
export MSB_PORT=25565
export MSB_PREFIX="!"
export MSB_INTERVAL=30 # Interval (seconds) for uptime check
export MSB_CHANNEL="" # Channel for uptime announcment (leave blank for none)
```

Start the bot with:
```sh
$ ./start.sh
```
