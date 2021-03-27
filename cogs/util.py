import discord
from discord.ext import commands

class Util(commands.Cog):

  def __init__(self, client):
    self.client = client

  @commands.command()
  async def help(self, ctx):
    embed = discord.Embed(colour=discord.Colour(0xf5a623), timestamp=datetime.datetime.utcnow())
    embed.add_field(name=".find <search term>", value="replace <search term> with author, title, isbn, or anything really. Archivist will attempt to find your book!\n", inline=False)
    embed.add_field(name=".find <search term -language>", value='.find <your search term -english>. The default language is english if no flag is passed', inline=False)
    await ctx.send(embed=embed)

def setup(client):
  client.add_cog(Util(client))