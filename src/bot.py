import discord
import os
from dotenv import load_dotenv
import requests
from pokeapi import PokeAPIClient, PokemonType

dotenv_path = "../.env"  # insert your .env path here
load_dotenv(dotenv_path)

# instantiate a bot with the necessary intents
intents = discord.Intents.default()
intents.message_content = True  # lets the bot read messages
bot = discord.Client(intents=intents)
api_client = PokeAPIClient()

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

    if message.content.startswith('/type'):
        # splits the command into an array of strings
        message_array = message.content.split()

        # when len > 1 means there is a word after !gettype
        if len(message_array) > 1:
            response = api_client.get_pokemon_type(message_array)
            await message.channel.send(response[0])
        else:
            await message.channel.send('Type a pokemon name after')

    if message.content.startswith('/weakness'):
        message_array = message.content.split()
        description_text = api_client.get_type_multiplier(message_array, 'weaknesses')
        embed = discord.Embed(
            color=discord.Color.green(),
            description=description_text,
            title="Weaknesses: "
        )
        if len(message_array) > 1:
            await message.channel.send(embed=embed)
        else:
            await message.channel.send('Type a type name after')


bot.run(DISCORD_TOKEN)
