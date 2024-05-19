# This file we interact with the Pokémon API

import requests

"""
TODO: Implement a function that returns a Pokémon's type based on the Pokémon's name and prints it to console
using the requests library to interact with the Pokémon API
"""
@bot_event
async def on_message(message):
    if message.author == bot.user:
        return