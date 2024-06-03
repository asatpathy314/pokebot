import time
import json
from pokeapi import PokeAPIClient

# in order to use this you need to add ", data_response['name']" to the return in get_type_multiplier in pokeapi.py

client = PokeAPIClient()  # instantiate a new client
return_dict = dict()  # create a dictionary to store the data


for i in range(1, 1026):
    message_array = ['/weakness', str(i)]
    relation = 'weaknesses'
    weaknesses, original_pokemon_name, pokesprite, return_code, pokemon_name = client.get_type_multiplier(message_array, relation)
    print(i)
    return_dict |= {pokemon_name: {"weaknesses": weaknesses, "sprite": pokesprite}}
    time.sleep(0.1)

json.dump(return_dict, open("web.json", "w"))
print("Finished populating web.json")
