# This file we interact with the Pokémon API
import requests
from enum import Enum

class PokemonType(Enum):
    NORMAL = 1
    FIGHTING = 2
    FLYING = 3
    POISON = 4
    GROUND = 5
    ROCK = 6
    BUG = 7
    GHOST = 8
    STEEL = 9
    FIRE = 10
    WATER = 11
    GRASS = 12
    ELECTRIC = 13
    PSYCHIC = 14
    ICE = 15
    DRAGON = 16
    DARK = 17
    FAIRY = 18
    @staticmethod
    def from_str(label):
        return PokemonType[label.upper()].value

class PokeAPIClient:
    @staticmethod
    def get_pokemon_type(message_array):
        original_pokemon_name = ' '.join(message_array[1:])
        raw_pokemon_name = '-'.join(message_array[1:])
        pokemon_name = ''.join(filter(lambda x: x.isalnum() or x == '-', raw_pokemon_name))
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}")
        if response.status_code == 200:
            data = response.json()
            types = [type_info['type']['name'] for type_info in data['types']]
            return types, 0
        elif response.status_code == 404:
            return f'{original_pokemon_name} is not a Pokémon, please try again.', -1
        else:
            return f'An error occurred, please try again.', -2


    @staticmethod
    def get_type_weaknesses(message_array):
        type_request_response = PokeAPIClient.get_pokemon_type(message_array)
        if type_request_response[1] < 0:
            return type_request_response[0]
        type_array = type_request_response[0]
        responses = [requests.get(f"https://pokeapi.co/api/v2/type/{PokemonType.from_str(pokemon_type)}") for pokemon_type in type_array]
        if len(type_array) > 1:
            # TODO: handle the case where there are multiple types
            pass
        return [response.json().get('damage_relations') for response in responses]