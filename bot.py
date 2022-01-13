import os
import asyncio
import discord
import league_scrape, val_scrape

import selenium.common.exceptions

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from discord.ext import commands
from discord_slash import SlashCommand, SlashContext

from multiprocessing.pool import ThreadPool

opts = Options()
opts.headless = True
webdriver = webdriver.Chrome(options=opts)

token = os.environ.get('bot_token')

client = commands.Bot(command_prefix='?')
slash = SlashCommand(client, sync_commands=True)
pool = ThreadPool(processes=1)


@client.event
async def on_ready():
    activity = discord.Game(name="straightest jojo fan")
    await client.change_presence(activity=activity)
    print(f'{client.user} has connected to Discord!')


@slash.slash(
    name="repeat",
    description="repeats given string n-times"
)
async def _repeat(ctx: SlashContext, args, num):
    for i in range(int(num)):
        await asyncio.sleep(float(num))
        await ctx.send(args)


@slash.slash(
    name="test",
    description="testing"
)
async def _bb(ctx: SlashContext):
    await ctx.send('t')


@slash.slash(
    name="league",
    description="currently broke as balls"
)
async def _league(ctx: SlashContext, username, region):
    name = username
    username = username.replace(" ", "%20")
    username = username.replace("#", "%23")
    embed = discord.Embed()

    if region.lower() != 'kr':
        webdriver.get(f'https://{region.lower()}.op.gg/summoner/userName={username}')
    else:
        webdriver.get(f'https://www.op.gg/summoner/userName={username}')

    try:
        winrate = webdriver.find_element_by_css_selector('#SummonerLayoutContent > div.tabItem.Content.SummonerLayoutContent.summonerLayout-summary > div.SideContent > div.TierBox.Box > div > div.TierRankInfo > div.TierInfo > span.WinLose > span.winratio')
        wins = webdriver.find_element_by_css_selector('#SummonerLayoutContent > div.tabItem.Content.SummonerLayoutContent.summonerLayout-summary > div.SideContent > div.TierBox.Box > div > div.TierRankInfo > div.TierInfo > span.WinLose > span.wins')
        rank = webdriver.find_element_by_css_selector('#SummonerLayoutContent > div.tabItem.Content.SummonerLayoutContent.summonerLayout-summary > div.SideContent > div.TierBox.Box > div > div.TierRankInfo > div.TierRank')

        rank = rank.text

        if rank.lower() == 'challenger' or rank.lower() == 'master' or rank.lower() == 'grandmaster':
            rank = rank + '_1'

        embed = discord.Embed(title=name, description=region.upper())
        embed.add_field(name="Wins", value=wins.text.strip('W'))
        embed.add_field(name='Win Rate', value=winrate.text[9:])
        embed.set_image(url=f'https://opgg-static.akamaized.net/images/medals/{rank.replace(" ","_").lower()}.png?image=q_auto:best&v=1')
        await ctx.send(embed=embed)

    except selenium.common.exceptions.NoSuchElementException:
        await ctx.send(f'{name} is unranked or does not exist D:')


@slash.slash(
    name="val",
    description="A valorant competitive profile lookup, args: {username}#{region} ex. slimslam#NA1"
)
async def _val(ctx: SlashContext, username):
    try:
        embed = val_scrape.val(username)
        await ctx.send(embed=embed)
    except discord.errors.NotFound:
        await ctx.send('Something went wrong, try again (404 Not Found (error code: 10062): Unknown interaction')

client.run(token)

