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
client = commands.Bot(command_prefix = ".")

client.remove_command("help")

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