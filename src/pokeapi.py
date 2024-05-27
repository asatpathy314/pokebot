# This file we interact with the Pokémon API
import requests
import logging
import json
import copy
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
    def from_str(label: str):
        return PokemonType[label.upper()].value

    @staticmethod
    def to_str(num: int):
        return PokemonType(num).name.lower()


class PokeAPIClient:
    def __init__(self):
        self.strengths = json.load(open("strengths.json", "r"))
        self.weaknesses = json.load(open("weaknesses.json", "r"))
        self.default = {"normal": 1.0,  # do not mutate this dictionary
                        "fire": 1.0,
                        "water": 1.0,
                        "grass": 1.0,
                        "flying": 1.0,
                        "fighting": 1.0,
                        "poison": 1.0,
                        "ground": 1.0,
                        "rock": 1.0,
                        "psychic": 1.0,
                        "electric": 1.0,
                        "ice": 1.0,
                        "bug": 1.0,
                        "ghost": 1.0,
                        "steel": 1.0,
                        "dragon": 1.0,
                        "dark": 1.0,
                        "fairy": 1.0}

    @staticmethod
    def sanitize_message(message_array: list):
        original_message = ' '.join(message_array[1:])
        raw_message = '-'.join(message_array[1:])
        query = ''.join(filter(lambda x: x.isalnum() or x == '-', raw_message))
        return original_message, query

    @staticmethod
    def get_pokemon_type(message_array: list):
        original_pokemon_name, pokemon_name = PokeAPIClient.sanitize_message(message_array)
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}")
        if response.status_code == 200:
            data = response.json()
            types = [type_info['type']['name'] for type_info in data['types']]
            return types, 0
        elif response.status_code == 404:
            return f'{original_pokemon_name} is not a Pokémon, please try again.', -1
        else:
            return f'An error occurred, please try again.', -2

    def get_type_multiplier(self, message_array: list, relation: str, is_move: bool = False):
        if relation not in ["strengths", "weaknesses"]:
            logging.error("Invalid type relation. Please choose either 'strengths' or 'weaknesses'.")
            return -1
        if is_move:
            original_move_name, move_name = PokeAPIClient.sanitize_message(message_array)
            move_type = PokeAPIClient.get_move_type(move_name)
            if move_type == f'{move_name} is not a Pokémon move, please try again.':
                move_type = f'{original_move_name} is not a Pokémon move, please try again.'
                return move_type, -1
            else:
                return self.strengths[move_type] if relation == "strengths" else self.weaknesses[move_type], 0
        else:
            types_response, return_code = self.get_pokemon_type(message_array)
            if return_code < 0:
                return types_response
            new_state = copy.deepcopy(self.default)
            for pokemon_type in types_response:
                weakness_multipliers = self.weaknesses[pokemon_type].items()
                for type_string, multiplier in weakness_multipliers:
                    new_state[type_string] *= multiplier
            return new_state

    @staticmethod
    def get_move_type(move_name: str):
        response = requests.get(f"https://pokeapi.co/api/v2/move/{move_name}")
        if response.status_code == 200:
            data = response.json()
            return data['type']['name']
        elif response.status_code == 404:
            return f'{move_name} is not a Pokémon move, please try again.'
        else:
            return f'An error occurred, please try again.'
