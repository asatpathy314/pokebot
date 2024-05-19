import discord
import os
from dotenv import load_dotenv

dotenv_path = "../.env" # insert your .env path here
load_dotenv(dotenv_path)

# instantiate a bot with the necessary intents
intents = discord.Intents.default()
intents.message_content = True # lets the bot read messages
bot = discord.Client(intents=intents)

DISCORD_TOKEN = os.environ.get("DISCORD_API_TOKEN")

# event listener for when bot switches to online mode

@bot.event
async def on_ready():
    guild_counter = len(bot.guilds)

    for guild in bot.guilds:
        print(f'{bot.user} is connected to {guild}.')

    print(f'PokéBot is connected to {guild_counter} servers!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('!hello'):
        await message.channel.send('Hello!')

bot.run(DISCORD_TOKEN)