# The goal of this file is to get an "objects.json" file containing all traits, blessings,
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
json_file.close()
