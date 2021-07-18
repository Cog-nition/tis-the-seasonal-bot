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


@client.command()
@commands.has_permissions(administrator=True)
async def deletelist(ctx):
    channel = client.get_channel(ctx.channel.id)
    async for message in channel.history(limit=200):
        if message.author == client.user:
            await message.delete()

client.run(TOKEN)
