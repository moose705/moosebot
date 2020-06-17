import json
import random


def random_color():
    HEX_CHARS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"]
    color_string = ""
    return color_string.join(random.choices(HEX_CHARS, k=6))


def get_dict_from_json(name):
    json_file = open(name, "r")
    json_string = json_file.read()
    json_file.close()
    if json_string:
        return json.loads(json_string)
    else:
        return {}


party = get_dict_from_json("party.json")
npcs = get_dict_from_json("npcs.json")
world = get_dict_from_json("world.json")

def dict_to_json(dict_i, json_i):
    json_file = open(json_i, "w")
    json_string = json.dumps(dict_i)
    json_file.write(json_string)
    json_file.close()


def backup_party():
    dict_to_json(party, "party.json")


def backup_npcs():
    dict_to_json(npcs, "npcs.json")


def backup_characters():
    backup_party()
    backup_npcs()


def backup_wizards(wizards):
    dict_to_json(wizards, "wizards.json")


def backup_world(world):
    dict_to_json(world, "world.json")


next_name = None
next_short_name = None
next_backstory = None


def find_character(name):
    if name in party:
        return party[name]
    elif name in npcs:
        return npcs[name]
    else:
        return None
