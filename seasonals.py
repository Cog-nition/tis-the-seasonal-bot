import os
import discord
from discord.ext import commands
from get_anime_list import pull_airing_data
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(
        f'{client.user} has connected.:\n'
    )

@client.command()
@commands.has_permissions(administrator=True)
async def postseasonallist(ctx):
    await ctx.send("Generating list of shows, one moment...")
    list = pull_airing_data()
    for format in list:
        await ctx.send("**__{0}__**".format(format))
        for show in list[format]:
            name = show["data"]["Media"]["title"]["romaji"]
            await ctx.send(name)
        await ctx.send("** **")


client.run(TOKEN)
