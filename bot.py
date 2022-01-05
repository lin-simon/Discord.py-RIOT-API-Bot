import os
import asyncio
import discord

import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from discord.ext import commands
from multiprocessing.pool import ThreadPool

opts = Options()
opts.headless = True
webdriver = webdriver.Chrome(options=opts)

token = os.environ.get('bot_token')

client = commands.Bot(command_prefix='?')
pool = ThreadPool(processes=1)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.command()
async def repeat(ctx, args, num):
    for i in range(num):
        await asyncio.sleep(float(num))
        await ctx.send(args)

@client.command()
async def league(ctx, username, region):
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



@client.command()
async def val(ctx, username, *gamemode):
    username = username.replace(" ", "%20")
    username = username.replace("#", "%23")
    embed = discord.Embed()

    if "unrated" in gamemode:
        webdriver.get(f'https://tracker.gg/valorant/profile/riot/{username}/overview?playlist=unrated&season=all')
    else:
        webdriver.get(f'https://tracker.gg/valorant/profile/riot/{username}/overview?playlist=competitive&season=all')
        rank = webdriver.find_element_by_css_selector('#app > div.trn-wrapper > div.trn-container > div > main > div.content.no-card-margin > div.site-container.trn-grid.trn-grid--vertical.trn-grid--small > div.trn-grid.container > div.segment-stats.area-main-stats.card.bordered.header-bordered.responsive > div.highlighted.highlighted--giants > div.highlighted__content > div > div.valorant-highlighted-content__stats > img')


    wins = webdriver.find_element_by_css_selector('#app > div.trn-wrapper > div.trn-container > div > main > div.content.no-card-margin > div.site-container.trn-grid.trn-grid--vertical.trn-grid--small > div.trn-grid.container > div.segment-stats.area-main-stats.card.bordered.header-bordered.responsive > div.main > div.stat.align-left.expandable.feature-hint > div > div.numbers > span.value')
    winrate = webdriver.find_element_by_css_selector('#app > div.trn-wrapper > div.trn-container > div > main > div.content.no-card-margin > div.site-container.trn-grid.trn-grid--vertical.trn-grid--small > div.trn-grid.container > div.segment-stats.area-main-stats.card.bordered.header-bordered.responsive > div.giant-stats > div:nth-child(4) > div > div.numbers > span.value')
    #accuracy = webdriver.find_element_by_css_selector('#app > div.trn-wrapper > div.trn-container > div > main > div.content.no-card-margin > div.site-container.trn-grid.trn-grid--vertical.trn-grid--small > div.trn-grid.container > div.accuracy.accuracy > div > div > table > tbody > tr:nth-child(1) > td:nth-child(2)')
    tag = webdriver.find_element_by_css_selector('#app > div.trn-wrapper > div.trn-container > div > main > div.content.no-card-margin > div.ph > div.ph__container > div.ph-details > div.ph-details__identifier > span > span.trn-ign__discriminator')
    name = webdriver.find_element_by_css_selector('#app > div.trn-wrapper > div.trn-container > div > main > div.content.no-card-margin > div.ph > div.ph__container > div.ph-details > div.ph-details__identifier > span > span.trn-ign__username')

    embed = discord.Embed(title=name.text, description=tag.text)
    embed.add_field(name="Wins", value=wins.text)
    embed.add_field(name="Win %", value=winrate.text)
    #embed.add_field(name="Headshot %", value=accuracy.text)
    embed.set_image(url=rank.get_attribute('src'))

    await ctx.send(embed=embed)

client.run(token)
