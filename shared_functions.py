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

# refactor below into one or two functions taking name of json, name of dict

def backup_party():
  json_file = open("party.json", "w")
  json_string = json.dumps(party)
  json_file.write(json_string)
  json_file.close()

def backup_npcs():
  json_file = open("npcs.json", "w")
  json_string = json.dumps(npcs)
  json_file.write(json_string)
  json_file.close()

def backup_characters():
  backup_party()
  backup_npcs()

def backup_wizards(wizards):
  wizards_json_string = json.dumps(wizards)
  wizards_json = open("wizards.json", "w")
  wizards_json.write(wizards_json_string)
  wizards_json.close()

def backup_world(world):
  json_file = open("world.json", "w")
  json_string = json.dumps(world)
  json_file.write(json_string)
  json_file.close()

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
