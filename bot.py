import os
import discord
import league_fetch, val_scrape

from discord.ext import commands
from discord_slash import SlashCommand, SlashContext

from multiprocessing.pool import ThreadPool

client = commands.Bot(command_prefix='?')   
slash = SlashCommand(client, sync_commands=True)
pool = ThreadPool(processes=1)

TOKEN = os.getenv('bot_token')

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="straightest jojo fan"))
    print(f'{client.user} has connected to Discord!')


@slash.slash(
    name="league",
    description="A League of Legends ranked profile lookup, args: {username}, {region}, ex. slimslam, NA1"
)
async def _league(ctx: SlashContext, username, region):
    try:
        embed = await league_fetch.league(username, region)
        message = await ctx.send(embed=embed)
        await message.add_reaction('⬅️')
        await message.add_reaction('➡️')
        
    except discord.errors.NotFound:
        await ctx.send('Something went wrong.')

    @client.event
    async def on_reaction_add(reaction,user):
        if user != client.user:
            await reaction.message.edit(embed=await val_scrape.val(username, 'na1'))

@slash.slash(
    name="val",
    description="A valorant competitive profile lookup, args: {username}, {region}, ex. slimslam, NA1"
)
async def _val(ctx: SlashContext, username, region):

    try:
        embed = await val_scrape.val(username,region)
        message = await ctx.send(embed=embed)
        await message.add_reaction('⬅️')
        await message.add_reaction('➡️')
    
    except discord.errors.NotFound:
        await ctx.send('Something went wrong, try again (404 Not Found (error code: 10062): Unknown interaction')

    @client.event
    async def on_reaction_add(reaction,user):
        if user != client.user:
            await reaction.message.edit(embed=await league_fetch.league(username, region))
            
client.run(TOKEN)