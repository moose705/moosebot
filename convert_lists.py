
import random_lists
import shared_functions
import items

npcs = shared_functions.get_dict_from_json("npcs.json")
npcs_new = {}


def generate_new_json():
    for npc in npcs.items():
        name = npc[0]
        data = npc[1]
        inventory = data["Inventory"]
        item_names = []
        for item in inventory:
            item_name = item.split(":")[0]
            try:
                items.item_dict[item_name]
            except KeyError:
                if item_name != "Empty Slot" and item_name != "Empty slot" and item_name != " Empty slot":
                    print("Item not found: ", item_name)
            if item_name == "Empty slot" or item_name == "Empty Slot":
                item_name = 0
            if item_name == "????":
                item_name = (await items.random_item()).name
            item_names.append(item_name)
        data["Inventory"] = item_names
        # Conversions:
        # - ???? to a random, hidden item
        # Some sort of Empty Slot handling. Convert to 0?
        # How are we dealing with hidden items?
        npcs_new[name] = data

    shared_functions.dict_to_json(npcs_new, "npcs_new.json")


generate_new_json()

"""# The goal of this file is to get an "objects.json" file containing all traits, blessings,
# effects and items.

import json
import random_lists

big_item_dict = {}

item_lists = [random_lists.CursedItems, random_lists.AwfulItems, random_lists.MehItems,
              random_lists.GoodItems, random_lists.GreatItems, random_lists.GodlyItems]

for item_list in item_lists:
    for item in item_list:
        name = item.split(":")[0]
        try:
            desc = item.split(":")[1]
        except IndexError:
            print(item)
        big_item_dict[name] = {}
        big_item_dict[name]["description"] = desc
        big_item_dict[name]["damage"] = 1
        big_item_dict[name]["quality"] = item_lists.index(item_list)
        big_item_dict[name]["uses"] = -1

json_file = open("items.json", "w")
json_string = json.dumps(big_item_dict)
json_file.write(json_string)
json_file.close()"""