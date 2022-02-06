import os
import time
import discord
from riotwatcher import LolWatcher, ApiError

API_TOKEN = os.environ.get('RIOT_API')
EMBED_ICON = 'https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/assets/splashscreens/lol_icon.png'

watcher = LolWatcher(API_TOKEN)

async def ranked(userid,region):
    ranked_stats = watcher.league.by_summoner(region,userid)
    if len(ranked_stats) == 3:
        return ranked_stats[2]['tier'], ranked_stats[2]['rank'], ranked_stats[2]['wins'], ranked_stats[2]['losses']
    return ranked_stats[0]['tier'], ranked_stats[0]['rank'], ranked_stats[0]['wins'], ranked_stats[0]['losses']

async def league(username,region):
    player = watcher.summoner.by_name(region,username)
    tier, rank, wins, losses = await ranked(player['id'],region)
    winrate = str(wins/(wins+losses))[2:4] + '%'
    level = player['summonerLevel']
    icon = f"http://ddragon.leagueoflegends.com/cdn/11.22.1/img/profileicon/{player['profileIconId']}.png"
    league_embed = discord.Embed(title=region.upper(), color=0xffDC00)
    league_embed.add_field(name='Wins', value=wins)
    league_embed.add_field(name="Winrate", value=winrate)
    league_embed.add_field(name="Level", value=level)
    league_embed.add_field(name="Rank: ", value=tier + '\t' + rank)
    league_embed.set_thumbnail(url=icon)
    league_embed.set_author(name=username,icon_url=EMBED_ICON)
        
    return league_embed