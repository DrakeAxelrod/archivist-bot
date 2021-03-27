import re
from isbntools.app import *
import urllib.request
import json
import re
import random
import datetime
import discord
from discord.ext import commands
from google_trans_new import google_translator

class Search(commands.Cog):
  base_api_link = "https://www.googleapis.com/books/v1/volumes?q=isbn:"
  translator = google_translator()

  def __init__(self, client):
    self.client = client


  def strip_symbols(self, ctx, strip_string):
    a = re.sub('&quot;', '"', strip_string)
    b = re.sub('&#39;', "'", a)
    c = re.sub('--Provided in synopsis.|Provided in synopsis.', "", b)
    return c
  
  def lang_code(self, ctx, string):
    formated_string = string.capitalize()
    with open('./languages.json') as json_lang:
      langs = json.load(json_lang)
      return langs[formated_string]

  def seperateArgs(self, ctx, args, delimeter):
    finalArgs = []
    toAppend = ''
    index = 0
    for i in args:
        if(i == delimeter):
            finalArgs.append(toAppend.strip())
            toAppend = ''
        else:
            toAppend += i
        if(index == len(args) - 1):
            finalArgs.append(toAppend.strip())
            toAppend = ''
        index += 1
    return finalArgs

  @commands.command()
  async def find(self, ctx, *,question):
    string = str(question)
    print(string)
    args = self.seperateArgs(ctx, string, "-")

    get_isbn = isbn_from_words(args[0])
    if len(args) > 1:
      lang = self.lang_code(ctx, args[1])
    else:
      lang = 'en'
    with urllib.request.urlopen(self.base_api_link + get_isbn) as f:
      query = f.read()

    decoded_query = query.decode("utf-8")
    data = json.loads(decoded_query) # deserializes decoded_query to a Python dataect
    if data['totalItems'] > 0:
      results = data["items"][0] 
      if "authors" in results["volumeInfo"]:
        authors_data = results["volumeInfo"]["authors"]
      else:
        author_data = "unknown"
      
      # image_url = results["volumeInfo"]["imageLinks"]["thumbnail"]
      # book_title = results["volumeInfo"]["title"]
      # authors = ",\n".join(authors_data)
      # public_domain = results["accessInfo"]["publicDomain"]
      # page_count = results["volumeInfo"]["pageCount"]
      # description = results["volumeInfo"]["description"]
      # print("web url: " + str(weblink))
      # print("img url: " + str(image_url))
      # print("title: " + str(book_title))
      # print("author: " + str(authors))
      # print("domain: " + str(public_domain))
      # print("pg: " + str(page_count))
      # print("description: " + str(description))

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
        pre_title = results["volumeInfo"]["title"]
        original_lang = self.translator.detect(pre_title)
        title = self.translator.translate(pre_title, lang_tgt=lang)
        embed.add_field(name="Original Language", value=f"{original_lang[1]} - {original_lang[0]}", inline=False)
        embed.add_field(name="Title", value=title, inline=False)

      embed.add_field(name="ISBN", value=get_isbn, inline=False)
      embed.add_field(name="Authors", value=",\n".join(authors_data), inline=True)

      if "publicDomain" in results["accessInfo"]:
        embed.add_field(name="Public Domain ", value=results["accessInfo"]["publicDomain"], inline=True)

      if "pageCount" in results["volumeInfo"]:
        embed.add_field(name="Page count", value=results["volumeInfo"]["pageCount"], inline=True)

      if "description" in results["volumeInfo"]:
        pre_description = results["volumeInfo"]["description"]
        description = self.translator.translate(pre_description, lang_tgt=lang)
        embed.add_field(name="Summary", value=description)

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