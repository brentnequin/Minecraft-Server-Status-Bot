import discord
from discord.ext import commands
import os
import requests

command_prefix = "."
client = commands.Bot(command_prefix=command_prefix)
token = os.getenv("DISCORD_BOT_TOKEN")

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle)
    print("I am online")

@client.command(name="ping", help="Ping the bot")
async def ping(ctx):
    await ctx.send(f"🏓 Pong with {str(round(client.latency, 2))}")

@client.command(name="status")
async def server_status(ctx, arg=None):
    if arg == None:
        await ctx.send(f"Please provide a server address: .set <address>.")
    else:
        address = arg
        url = ''.join(['https://api.mcsrvstat.us/2/', address])
        response = requests.get(url=url)
        data = response.json()

        if data['port'] == '':
            await ctx.send(f"Invalid server address (%s)." % (address))
        else:
            if 'hostname' in data:
                server_name = data['hostname']
            else:
                server_name = data['ip']

            if data['online'] == False:
                embedVar = discord.Embed(title=server_name, color=0x00ff00)
                embedVar.add_field(name="Status", value="🔴 Offline", inline=True)
                embedVar.add_field(name="Port", value=data['port'], inline=True)
                await ctx.send(embed=embedVar)
            else:
                embedVar = discord.Embed(title=server_name, description=data['motd']['clean'][0], color=0x00ff00)
                embedVar.add_field(name="Status", value="🟢 Online", inline=True)
                embedVar.add_field(name="Port", value=data['port'], inline=True)
                embedVar.add_field(name="Online", value="%s / %s" % (data['players']['online'], data['players']['max']), inline=True)
                if 'list' in data['players']:
                    embedVar.add_field(name="Players", value=', '.join(data['players']['list']), inline=False)
                await ctx.send(embed=embedVar)
        
client.run(token)
