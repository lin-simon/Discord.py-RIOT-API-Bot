import discord
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

opts = Options()
opts.headless = True
webdriver = webdriver.Chrome(options=opts)


class Embed:
    def __init__(self, username, name, wins, winrate, rank, banner, tag, agent, agent_name, playtime, url):
        self.username = username
        self.name = name
        self.wins = wins
        self.winrate = winrate
        self.rank = rank
        self.banner = banner
        self.tag = tag
        self.agent = agent
        self.agent_name = agent_name
        self.playtime = playtime
        self.url = url

        self.colour = 0xff2400


async def val(username, region='na1'):
    user = username
    username = username + '%23' + region
    username = username.replace(" ", "%20")
    url = f'https://tracker.gg/valorant/profile/riot/{username}/overview?playlist=competitive&season=all'
    webdriver.implicitly_wait(5)
    webdriver.get(url)
    
    rank = webdriver.find_element_by_css_selector('#app > div.trn-wrapper > div.trn-container > div > main > div.content.no-card-margin > div.site-container.trn-grid.trn-grid--vertical.trn-grid--small > div.trn-grid.container > div.segment-stats.area-main-stats.card.bordered.header-bordered.responsive > div.highlighted.highlighted--giants > div.highlighted__content > div > div.valorant-highlighted-content__stats > img')
    wins = webdriver.find_element_by_css_selector('#app > div.trn-wrapper > div.trn-container > div > main > div.content.no-card-margin > div.site-container.trn-grid.trn-grid--vertical.trn-grid--small > div.trn-grid.container > div.segment-stats.area-main-stats.card.bordered.header-bordered.responsive > div.main > div.stat.align-left.expandable.feature-hint > div > div.numbers > span.value')
    winrate = webdriver.find_element_by_css_selector('#app > div.trn-wrapper > div.trn-container > div > main > div.content.no-card-margin > div.site-container.trn-grid.trn-grid--vertical.trn-grid--small > div.trn-grid.container > div.segment-stats.area-main-stats.card.bordered.header-bordered.responsive > div.giant-stats > div:nth-child(4) > div > div.numbers > span.value')
    tag = webdriver.find_element_by_css_selector('#app > div.trn-wrapper > div.trn-container > div > main > div.content.no-card-margin > div.ph > div.ph__container > div.ph-details > div.ph-details__identifier > span > span.trn-ign__discriminator')
    name = webdriver.find_element_by_css_selector('#app > div.trn-wrapper > div.trn-container > div > main > div.content.no-card-margin > div.ph > div.ph__container > div.ph-details > div.ph-details__identifier > span > span.trn-ign__username')
    agent = webdriver.find_element_by_css_selector(('#app > div.trn-wrapper > div.trn-container > div > main > div.content.no-card-margin > div.site-container.trn-grid.trn-grid--vertical.trn-grid--small > div.trn-grid.container > div.top-agents.area-top-agents > div > div > table > tbody > tr:nth-child(1) > td:nth-child(1) > div > img'))
    agent_name = webdriver.find_element_by_css_selector('#app > div.trn-wrapper > div.trn-container > div > main > div.content.no-card-margin > div.site-container.trn-grid.trn-grid--vertical.trn-grid--small > div.trn-grid.container > div.top-agents.area-top-agents > div > div > table > tbody > tr:nth-child(1) > td:nth-child(1) > div > span')
    playtime = webdriver.find_element_by_css_selector('#app > div.trn-wrapper > div.trn-container > div > main > div.content.no-card-margin > div.site-container.trn-grid.trn-grid--vertical.trn-grid--small > div.trn-grid.container > div.top-agents.area-top-agents > div > div > table > tbody > tr:nth-child(1) > td:nth-child(2) > div > span')
    banner = webdriver.find_element_by_css_selector('#app > div.trn-wrapper > div.trn-container > div > main > div.content.no-card-margin > div.ph > div.ph__container > div.ph-avatar > svg > image')

    embed = Embed(user,
                  name.text,
                  wins.text,
                  winrate.text,
                  rank.get_attribute('src'),
                  banner,
                  tag.text,
                  agent.get_attribute('src'),
                  agent_name.text,
                  playtime.text,
                  url)

    val_embed = discord.Embed(title=embed.name, color=embed.colour)
    val_embed.add_field(name="Wins", value=embed.wins)
    val_embed.add_field(name="Win %", value=embed.winrate)
    val_embed.set_image(url=embed.rank)
    val_embed.set_thumbnail(url=banner.get_attribute('href'))
    val_embed.set_footer(text=f"Most played agent: {embed.agent_name} - {embed.playtime}", icon_url=embed.agent)
    val_embed.set_author(name=embed.username, url=embed.url, icon_url="https://static.wikia.nocookie.net/leagueoflegends/images/8/88/Valorant_icon.png/revision/latest?cb=20210118012928")

    return val_embed