import discord
from discord.ext import commands
import os
from isbntools.app import *
import urllib.request
import json
import datetime
import textwrap

access_token = os.environ["ACCESS_TOKEN"]

client = commands.Bot(command_prefix = ".")
base_api_link = "https://www.googleapis.com/books/v1/volumes?q=isbn:"

client.remove_command("help")

@client.event
async def on_ready() :
    await client.change_presence(status = discord.Status.idle, activity = discord.Game("Reading"))
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.command()
async def find(ctx, *, title):
  get_isbn = isbn_from_words(title)
  
  try:
    with urllib.request.urlopen(base_api_link + get_isbn) as f:
          text = f.read()
    decoded_text = text.decode("utf-8")
    obj = json.loads(decoded_text) # deserializes decoded_text to a Python object
    volume_info = obj["items"][0] 
    authors = obj["items"][0]["volumeInfo"]["authors"]

    embed = discord.Embed(colour=discord.Colour(0xf5a623), timestamp=datetime.datetime.utcnow())
    embed.add_field(name="Title", value=volume_info["volumeInfo"]["title"], inline=False)
    embed.add_field(name="ISBN", value=get_isbn, inline=true)
    embed.add_field(name="Authors", value=",\n".join(authors), inline=True)
    embed.add_field(name="Public Domain ", value=volume_info["accessInfo"]["publicDomain"], inline=True)
    embed.add_field(name="Page count", value=volume_info["volumeInfo"]["pageCount"])
    embed.add_field(name="Summary", value=volume_info["searchInfo"]["textSnippet"])
  except:
    await ctx.send("look I went to the Library of Alexandria and I could not find your book, I hate to ask but are you sure thats how it is spelled?")

  await ctx.send(embed=embed)

@client.command()
async def help(ctx):
  embed = discord.Embed(colour=discord.Colour(0xf5a623), timestamp=datetime.datetime.utcnow())
  embed.add_field(name=".find 'search term'", value="will make archivist attempt to find your book" )
  await ctx.send(embed=embed)

client.run(access_token)