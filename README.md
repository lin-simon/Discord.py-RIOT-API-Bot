# Discord.py RIOT API Bot
This is a Discord bot built using [Discord.py](https://discordpy.readthedocs.io/en/latest/) and the [RIOT GAMES API](https://developer.riotgames.com/apis) for online games League of Legends and VALORANT. It allows users to look up information about their account and view their normally inaccesible ranked stats in the game. The bot uses both RIOT API to read stats from JSON files and Selenium.py for webscraping various game assets to produce a visually appealing embedded display on discord.

# Prerequisites
To use this bot, you will need:

A Discord account and a server to add the bot to
A RIOT API key

# Setting up
To set up the bot, follow these steps:

```
Clone the repository: git clone https://github.com/lin-simon/Discord.py-RIOT-API-Bot.git
Navigate to the directory: cd Discord.py-RIOT-API-Bot
Install the dependencies: pip install -r requirements.txt

Create a file called **.env** and add your Discord and RIOT API keys in the following format:
DISCORD_TOKEN=your_discord_token
RIOT_API_KEY=your_riot_api_key

Run the bot: python bot.py
```

# Usage
This bot uses slash commands, a new feature of discord.py. Ensure you have downloaded the latest version of discord.py or ***version 2.0+.**

To use the bot, **type /val or /league <user_id> <region_name>** in a Discord channel where the bot has been added and provided permissions. The bot will return information about the RIOT ID, including their ranked stats and other player information for the current season.

# Customization
To customize the bot, you can edit the bot.py file and add additional commands using the Discord.py library. You can also edit the .env file to add additional environment variables.
