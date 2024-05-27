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
        message_array = message.content.split()
        if len(message_array) > 1:
            response, original_pokemon_name, return_code = api_client.get_pokemon(message_array)
            if return_code < 0:
                await message.channel.send(response)
                return
            types = [type_info['type']['name'].title() for type_info in response['types']]
            title_string = 'Types' if len(types) > 1 else 'Type'
            embed = discord.Embed(
                color=discord.Color.red(),
                title=original_pokemon_name.title() + ' ' + title_string
            )
            embed.add_field(name=title_string, value=', '.join(types), inline=False)
            embed.set_thumbnail(url=response['sprites']['front_default'])
            await message.channel.send(embed=embed)
        else:
            await message.channel.send('Type a pokemon name after')

    if message.content.startswith('/weakness'):
        message_array = message.content.split()
        if len(message_array) > 1:
            pass
        else:
            await message.channel.send('Type a pokemon name after')
            return
        type_multipliers, pokemon_name, pokemon_image, return_code = api_client.get_type_multiplier(message_array,
                                                                                                    'weaknesses')
        if return_code < 0:
            await message.channel.send(type_multipliers)
            return
        (four, two, one, half, quarter) = api_client.filter_weaknesses(type_multipliers)
        embed = discord.Embed(
            color=discord.Color.dark_red(),
            title=pokemon_name.title() + ' Weaknesses'
        )
        if four:
            embed.add_field(name="4x Weaknesses", value=', '.join([key.title() for key in four.keys()]),
                            inline=False)
        if two:
            embed.add_field(name="2x Weaknesses", value=', '.join([key.title() for key in two.keys()]),
                            inline=False)
        if one:
            embed.add_field(name="1x Weaknesses", value=', '.join([key.title() for key in one.keys()]),
                            inline=False)
        if half:
            embed.add_field(name="0.5x Weaknesses", value=', '.join([key.title() for key in half.keys()]),
                            inline=False)
        if quarter:
            embed.add_field(name="0.25x Weaknesses", value=', '.join([key.title() for key in quarter.keys()]),
                            inline=False)
        embed.set_thumbnail(url=pokemon_image)
        if len(message_array) > 1:
            await message.channel.send(embed=embed)
        else:
            await message.channel.send('Type a type name after')


bot.run(DISCORD_TOKEN)
