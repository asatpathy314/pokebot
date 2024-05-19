import discord
import os
from dotenv import load_dotenv
import requests
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

    if message.content.startswith('!gettype'):
        # splits the command into an array of strings
        mon = message.content.split()

        # when len > 1 means there is a word after !gettype
        if len(mon) > 1:
            poke = mon[1]
            # sends a request to the url and parses JSON content into python
            api = requests.get("https://pokeapi.co/api/v2/pokemon/" + poke)
            conv = api.json()

            # status code 200 means the pokemon exists
            if api.status_code == 200:
                # finds the "types" section on the API and goes through each type
                # and adds the name variable from each into types_str
                types = [type_info['type']['name'] for type_info in conv['types']]
                types_str = ', '.join(types)
                await message.channel.send(types_str)
            else:
                # this don't work yet
                await message.channel.send(f'{poke} is not a pokemon, please try again.')
        else:
            await message.channel.send('Type a pokemon name after')

bot.run(DISCORD_TOKEN)