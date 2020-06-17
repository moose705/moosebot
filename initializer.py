import shared_functions
import classes

# This is currently global and probably shouldn't be, although these are meant to be constants.

traits = shared_functions.get_dict_from_json("traits.json")
blessings = shared_functions.get_dict_from_json("blessings.json")
# effects = shared_functions.get_dict_from_json("effects.json")
items = shared_functions.get_dict_from_json("items.json")

trait_dict = {}
blessing_dict = {}
item_dict = {}

for trait in traits.keys():
    trait_dict[trait] = classes.Trait(traits[trait])

for blessing in blessings.keys():
    # this is messy and needs testing
    # json could contain them in any order, so this attempts to link both ways
    blessing_dict[blessing] = classes.Trait(traits[trait])
    if blessing[-7:].lower() == "level i":
        for blessing_1 in blessing_dict.keys():
            if blessing_1.lower() == blessing[0:-7].lower() + "level ii":
                blessing_dict[blessing_1].downgrade = blessing
                blessing.upgrade = blessing_1
    if blessing[-8:].lower() == "level ii":
        for blessing_1 in blessing_dict.keys():
            if blessing_1.lower() == blessing[0:-7].lower() + "level i":
                blessing_dict[blessing_1].upgrade = blessing
                blessing.downgrade = blessing_1
        for blessing_1 in blessing_dict.keys():
            if blessing_1.lower() == blessing[0:-9].lower() + "level iii":
                blessing_dict[blessing_1].downgrade = blessing
                blessing.upgrade = blessing_1
    if blessing[-9:].lower() == "level iii":
        for blessing_1 in blessing_dict.keys():
            if blessing_1.lower() == blessing[0:-7].lower() + "level ii":
                blessing_dict[blessing_1].upgrade = blessing
                blessing.downgrade = blessing_1

for item in items.keys():
    item_dict[item] = classes.Item(items[item]["description"], items[item]["damage"],
                                   items[item]["quality"], items[item]["uses"])

# The above loops should go through function pairing with a big data structure matching name to methods.
