import discord
from discord.ext import commands
import os
from isbntools.app import *
import urllib.request
import json
import re
import datetime
import dotenv 
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = commands.Bot(command_prefix = ".", help_command=None)

@client.command()
async def help(ctx):
  embed = discord.Embed(colour=discord.Colour(0xf5a623), timestamp=datetime.datetime.utcnow())
  embed.add_field(name=".find <search term>", value="replace <search term> with author, title, isbn, or anything really. Archivist will attempt to find your book!\n", inline=False)
  embed.add_field(name=".find <search term -language>", value='.find <your search term -english>. The default language is english if no flag is passed', inline=False)
  await ctx.send(embed=embed)

for filename in os.listdir("./cogs"):
  if filename.endswith(".py"):
    client.load_extension(f"cogs.{filename[:-3]}")


@client.event
async def on_ready():
  await client.change_presence(status = discord.Status.idle, activity = discord.Game("with books!"))
  print('Logged in as')
  print(client.user.name)
  print(client.user.id)
  print('------')

client.run(TOKEN)