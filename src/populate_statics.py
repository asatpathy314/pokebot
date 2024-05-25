import requests
import json
import copy
from pokeapi import PokemonType

final = {
    "normal": {},
    "fire": {},
    "water": {},
    "grass": {},
    "flying": {},
    "fighting": {},
    "poison": {},
    "ground": {},
    "rock": {},
    "psychic": {},
    "ice": {},
    "bug": {},
    "ghost": {},
    "steel": {},
    "dragon": {},
    "dark": {},
    "fairy": {}
}

default = {"normal": 1.0,
           "fire": 1.0,
           "water": 1.0,
           "grass": 1.0,
           "flying": 1.0,
           "fighting": 1.0,
           "poison": 1.0,
           "ground": 1.0,
           "rock": 1.0,
           "psychic": 1.0,
           "ice": 1.0,
           "bug": 1.0,
           "ghost": 1.0,
           "steel": 1.0,
           "dragon": 1.0,
           "dark": 1.0,
           "fairy": 1.0}


def populate_weaknesses():
    for index in range(1, 19):  # (1, 19)
        weaknesses = copy.deepcopy(default)
        type_name = PokemonType.to_str(index)
        response = requests.get(f"https://pokeapi.co/api/v2/type/{index}")
        data = response.json()
        for pokemon_type in data['damage_relations']['double_damage_from']:
            weaknesses[pokemon_type['name']] = 2.0
        for pokemon_type in data['damage_relations']['half_damage_from']:
            weaknesses[pokemon_type['name']] = 0.5
        for pokemon_type in data['damage_relations']['no_damage_from']:
            weaknesses[pokemon_type['name']] = 0.0
        final[type_name] = weaknesses
    print(final)
    with open("weaknesses.json", "w") as file:
        json.dump(final, file)


def populate_strengths():
    for index in range(1, 19):  # (1, 19)
        strengths = copy.deepcopy(default)
        type_name = PokemonType.to_str(index)
        response = requests.get(f"https://pokeapi.co/api/v2/type/{index}")
        data = response.json()
        for pokemon_type in data['damage_relations']['double_damage_to']:
            strengths[pokemon_type['name']] = 2.0
        for pokemon_type in data['damage_relations']['half_damage_to']:
            strengths[pokemon_type['name']] = 0.5
        final[type_name] = strengths

    print(final)
    with open("strengths.json", "w") as file:
        json.dump(final, file)

populate_weaknesses()
