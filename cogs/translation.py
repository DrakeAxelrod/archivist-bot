import discord
from discord.ext import commands
from google_trans_new import google_translator
import json

class Translation(commands.Cog):
  translator = google_translator()

  def __init__(self, client):
    self.client = client

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

  def lang_code(self, ctx, string):
    formated_string = string.capitalize()
    with open('./languages.json') as json_lang:
      langs = json.load(json_lang)
      return langs[formated_string]

  @commands.command()
  async def translate(self, ctx, *, string):
    args = self.seperateArgs(ctx, string, "-")
    if len(args) > 1:
      lang = self.lang_code(ctx, args[1])
    else:
      lang = 'en'
    reply = args[0]
    await ctx.send(self.translator.translate(reply, lang_tgt=lang))



def setup(client):
  client.add_cog(Translation(client))