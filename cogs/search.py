import re
from isbntools.app import *
import urllib.request
import json
import re
import random
import datetime
import discord
from discord.ext import commands

class Search(commands.Cog):

  def __init__(self, client):
    self.client = client


  def strip_symbols(strip_string):
    a = re.sub('&quot;', '"', strip_string)
    b = re.sub('&#39;', "'", a)
    c = re.sub('--Provided in synopsis.|Provided in synopsis.', "", b)
    return c

  @commands.command()
  async def find(self, ctx, *, question):
    get_isbn = isbn_from_words(question)

    base_api_link = BOOK_SEARCH_API
    # "https://www.googleapis.com/books/v1/volumes?q=isbn:"
  
    with urllib.request.urlopen(base_api_link + get_isbn) as f:
      query = f.read()

    decoded_query = query.decode("utf-8")
    data = json.loads(decoded_query) # deserializes decoded_query to a Python dataect
    if data['totalItems'] > 0:
      results = data["items"][0] 
      if "authors" in results["volumeInfo"]:
        authors_data = results["volumeInfo"]["authors"]
      else:
        author_data = "unknown"

      embed_color = discord.Colour(0xf5a623)
      time = datetime.datetime.utcnow()
      if "previewLink" in results["volumeInfo"]:
        weblink = results["volumeInfo"]["previewLink"]
        embed = discord.Embed(colour=embed_color, description=f"[More Information]({weblink})", timestamp=time)
      else:
        embed = discord.Embed(colour=embed_color, timestamp=time)
      if "imageLinks" in results["volumeInfo"]:
        embed.set_thumbnail(url=results["volumeInfo"]["imageLinks"]["thumbnail"])
      if "title" in results["volumeInfo"]:
        embed.add_field(name="Title", value=results["volumeInfo"]["title"], inline=False)
      embed.add_field(name="ISBN", value=get_isbn, inline=False)
      embed.add_field(name="Authors", value=",\n".join(authors_data), inline=True)
      if "publicDomain" in results["accessInfo"]:
        embed.add_field(name="Public Domain ", value=results["accessInfo"]["publicDomain"], inline=True)
      if "pageCount" in results["volumeInfo"]:
        embed.add_field(name="Page count", value=results["volumeInfo"]["pageCount"], inline=True)
      if "description" in results["volumeInfo"]:
        embed.add_field(name="Summary", value=results["volumeInfo"]["description"])
      await ctx.send(embed=embed)
    else:
      ran_search = ("checked", "looked in", "searched", "explored", "hunted throughout")
      ran_lib = ("The Library of Alexandria", "The Library of Ashurbanipal", "The Library of Pergamum", "The Villa of the Papyri", "The Libraries of Trajan’s Forum", "The Library of Celsus", "The Imperial Library of Constantinople", "The House of Wisdom")
      ran_request = ("Maybe","Perhaps","Possibly","Concievably","Perchance")
      ran_try = ("try","attempt","endeavor to use","test")
      ran_diff = ("different","seperate","non-identical","similar","interchangable","related","alike")
      n_1 = random.randrange(0,5)
      n_2 = random.randrange(0,7)
      n_3 = random.randrange(0,4)
      n_4 = random.randrange(0,3)
      n_5 = random.randrange(0,6)
      reply = f"So.. I {ran_search[n_1]} the archives, I even checked '{ran_lib[n_2]}'. {ran_request[n_3]} could you {ran_try[n_4]} a {ran_diff[n_5]} <search term>?"
      await ctx.send(reply)

def setup(client):
  client.add_cog(Search(client))