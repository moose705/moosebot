import os
import random
import sys

from dotenv import load_dotenv

import characters
import items
import names
import random_lists
import shared_functions
import traits
import wizard
from bot import bot as bot
from shared_functions import party as party
from shared_functions import npcs as npcs
from shared_functions import world as world

# below: laziness

load_dotenv()

TOKEN = os.getenv("TOKEN")

# Party & NPC Management

next_backstory = None
next_name = None
next_short_name = None


@bot.command(name='countitems')
async def count_items(ctx):
    await ctx.send("There are " + str(len(items.item_dict)) + " items currently in the item pool.")


@bot.command(name='countbackstories')
async def count_backstories(ctx):
    num_backstories = len(random_lists.Backstories)
    await ctx.send("There are " + str(num_backstories) + " backstories currently in the backstory pool.")


@bot.command(name='nextname')
async def next_name_function(ctx, name):
    global next_short_name
    global next_name
    next_short_name = name.split(" ")[0]
    if shared_functions.find_character(next_short_name) is not None:
        await ctx.send("A character already exists with the name " + next_short_name + ".")
        next_short_name = None
        return
    next_name = name


@bot.command(name='nextbackstory')
async def next_backstory_function(ctx, backstory):
    global next_backstory
    next_backstory = backstory


@bot.command(name='additem', aliases=["item"])
async def add_item(ctx, name, item):
    character = shared_functions.find_character(name)
    if not character:
        await ctx.send("Character does not exist!")
        return
    for i in range(0, len(character["Inventory"])):
        if character["Inventory"][i] == "Empty slot" or character["Inventory"][i] == "Empty Slot":
            character["Inventory"][i] = item
            break
    else:
        await ctx.send(name + "'s inventory is full!")
        return
    await ctx.send(embed=characters.print_character(name))


@bot.command(name='removeitem', aliases=["take", "drop"])
async def remove_item(ctx, name, item):
    character = shared_functions.find_character(name)
    if not character:
        await ctx.send("Character does not exist!")
        return
    length = len(item)
    for i in range(0, len(character["Inventory"])):
        print(character["Inventory"][i][0:length])
        if character["Inventory"][i][0:length] == item:
            character["Inventory"][i] = "Empty slot"
            break
    else:
        await ctx.send("Item not found.")
        return
    await ctx.send(embed=characters.print_character(name))


@bot.command(name='pay', aliases=["givemoney", "givegold"])
async def pay(ctx, name, gold):
    await increase(ctx, name, "Gold", gold)


@bot.command(name='increase', aliases=["increasestat", "boost", "booststat"])
async def increase(ctx, name, stat, number):
    try:
        number = int(number)
    except ValueError:
        await ctx.send("Stat must be increased by a number.")
        return
    character = shared_functions.find_character(name)
    if not character:
        await ctx.send("Character " + name + " does not exist")
        return
    if stat not in character:
        await ctx.send("Stat " + stat + " does not exist")
        return
    try:
        # prevent some jackass from crashing bot by trying to increase "Backstory"
        int(character[stat])
    except ValueError:
        await ctx.send("Are you trying to increase a non-numerical stat...?")
        return
    character[stat] += number
    await ctx.send(embed=characters.print_character(name))


@bot.command(name='decrease', aliases=["lowerstat", "decreasestat", "lower"])
async def decrease(ctx, name, stat, number):
    await increase(ctx, name, stat, -int(number))


@bot.command(name='damage', aliases=["hurt"])
async def damage(ctx, name, number):
    await decrease(ctx, name, "Health", number)
    character = shared_functions.find_character(name)
    if character and character["Health"] <= 0:
        await kill_char(ctx, name)


@bot.command(name='heal', aliases=["restore"])
async def heal(ctx, name, number=None):
    if number is not None:
        await increase(ctx, name, "Health", number)
    else:
        character = shared_functions.find_character(name)
        if not character:
            await ctx.send("Character " + name + " does not exist, dummy")
            return
        # hardcoded max health right now; will eventually need to change to a character["Max Health"] attribute if i
        # implement things like Blessing of Bloat
        characters.change_character_data(name, "Health", 2 * character["Strongness"] + 1)
        await ctx.send(embed=characters.print_character(name))


@bot.command(name='check', aliases=["statcheck"])
async def check(ctx, name, stat, required_number, global_modifier=0):
    try:
        required_number = int(required_number)
    except ValueError:
        target = shared_functions.find_character(required_number)
        if not target:
            await ctx.send("There is no character named " + required_number)
            return
        if stat not in target:
            await ctx.send(required_number + " has no stat " + stat)
            return
        required_number = target[stat]
        # get required_number from target stat.
    character = shared_functions.find_character(name)
    if not character:
        await ctx.send("There is no character named " + name)
        return
    try:
        global_modifier = int(global_modifier)
    except ValueError:
        await ctx.send("Modifier is not a number...")
        return
    if stat not in character:
        await ctx.send(name + " has no stat " + stat)
        return
    global_modifier += world["modifier"]
    roll = random.randint(1, 20)
    print(roll)
    passed = False
    if roll == 20:
        passed = True
    elif roll == 1:
        pass
    else:
        if (character[stat] - required_number) + roll + global_modifier >= 11:
            passed = True
    if passed:
        await ctx.send(stat + " check passed!")
    else:
        await ctx.send(stat + " check failed!")


@bot.command(name='combat', aliases=["fight", "attack"])
async def combat(ctx, name, weapon_damage, target, global_modifier=0, stat="Strongness"):
    damage_target = False
    try:
        defense = int(target)
    except ValueError:
        target_character = shared_functions.find_character(target)
        if not target_character:
            await ctx.send("Could not find target.")
            return
        if stat in target_character:
            defense = target_character[stat]
        else:
            await ctx.send("Stat does not exist.")
        damage_target = True
    try:
        global_modifier = int(global_modifier)
        weapon_damage = int(weapon_damage)
    except ValueError:
        await ctx.send("One of the numerical parameters was not a number.")
        return
    character = shared_functions.find_character(name)
    global_modifier += world["modifier"]
    if not character:
        await ctx.send("No character named " + name)
        return
    if stat not in character:
        await ctx.send("Invalid stat")
        return
    roll = random.randint(1, 20)
    print(roll)
    miss = False
    crit = 1
    if roll == 20:
        crit = 2
    if roll == 1:
        miss = True
    else:
        damage_done = (character[stat] - defense + roll + global_modifier - 10) * (weapon_damage * crit)
        if damage_done < 0:
            damage_done = 0
    if miss:
        await ctx.send("Missed!")
    else:
        if damage_target and damage_done > 0:
            await damage(ctx, target, damage_done)
        await ctx.send("Did " + str(damage_done) + " damage!")
        if crit > 1:
            await ctx.send("A critical hit!")


@bot.command(name='killchar', aliases=["kill", "nuke"])
async def kill_char(ctx, name):
    # TODO: Have a character drop their entire inventory upon being killed, activating any explosives.
    #  It would be pretty comical to randomly trigger %use (prompting for a target if necessary).

    # TODO: File away deceased characters in an additional dictionary for use with Necromancer.
    character = shared_functions.find_character(name)
    if not character:
        await ctx.send("Could not find party member or NPC named " + name)
        return
    if name in npcs.keys():
        relevant_dict = npcs
    else:
        relevant_dict = party
    # later: add to necromancy dictionary
    response = "**" + relevant_dict[name]["Name"] + " has been slain.**"
    for item in relevant_dict[name]["Inventory"]:
        if item != "Empty slot":
            response += "\nThe following item dropped: " + items.item_dict[item].print_teaser()
    relevant_dict.pop(name, False)
    shared_functions.backup_characters()
    await ctx.send(response)


@bot.command(name='party')
async def print_party(ctx, name=None):
    if not name:
        for character_name in party.keys():
            response = characters.print_character(character_name)
            await ctx.send(embed=response)
    else:
        response = characters.print_character(name)
        await ctx.send(embed=response)


@bot.command(name='npc')
async def npc(ctx, name=None):
    if not name:
        length = str(len(npcs.keys()))
        await ctx.send("There are currently " + length + " NPCs in the pool.")
        return
    if name == "all":
        for character in npcs:
            await ctx.send(embed=characters.print_character(character))
    else:
        await ctx.send(embed=characters.print_character(name))


@bot.command(name='randnpc')
async def randnpc(ctx):
    if len(npcs.keys()) == 0:
        await ctx.send("There are no NPCs!")
        return
    npc = random.choice(list(npcs.keys()))
    await ctx.send(embed=characters.print_character(npc))


@bot.command(name='recruit', aliases=["hire", "addparty"])
async def recruit(ctx, name):
    npc = npcs[name]
    npcs.pop(name)
    party[name] = npc
    shared_functions.backup_characters()
    await ctx.send(name + " added to party!")


@bot.command(name='fire', aliases=['retire', 'kick', 'ditch'])
async def leave(ctx, name):
    try:
        npc = party[name]
    except KeyError:
        await ctx.send("No party member named " + name)
        return
    party.pop(name)
    npcs[name] = npc
    await ctx.send(name + " removed from party!")
    shared_functions.backup_characters()


@bot.command(name='wipeparty')
async def wipe_party(ctx):
    global party
    party = {}
    shared_functions.backup_party()
    await ctx.send("Successfully killed entire party.")


@bot.command(name='retireparty', aliases=["giveup", "win"])
async def retire_party(ctx):
    for name in list(party.keys()):
        await leave(ctx, name)
    await advance(ctx, 1)
    await ctx.send("Entire party has been retired.")


@bot.command(name='inventorysize')
async def inventory_size(ctx, name, size):
    character = shared_functions.find_character(name)
    if not character:
        await ctx.send("Character does not exist!")
        return
    try:
        int(size)
    except ValueError:
        await ctx.send("That is not a number you moron!")
        return
    length = len(party[name]["Inventory"])
    if length > int(size):
        party[name]["Inventory"] = party[name]["Inventory"][0:int(size)]
    elif length < int(size):
        for i in range(length, int(size)):
            party[name]["Inventory"].append("Empty slot")
    else:
        await ctx.send("Character already has inventory of size " + size + ".")
        return
    await ctx.send(embed=characters.print_character(name))


@bot.command(name='restart')
async def restart(ctx):
    sys.exit()


@bot.command(name='go', aliases=['advance', 'nextworld'])
async def advance(ctx, reset=False):
    # future support: track actual world map position, take a direction as argument
    world["number"] += 1
    world["modifier"] = 1 - int(((world["number"] + 1) / 2))
    world["stat cap"] = world["number"] + 4
    world["boss stat cap"] = world["number"] + 6
    if reset:
        world["number"] = 1
        world["modifier"] = 1
        world["stat cap"] = 5
        world["boss stat cap"] = 7
    shared_functions.backup_world(world)
    await(ctx.send("World has been set to " + str(world["number"]) + " providing a boost of " + str(
        world["modifier"]) + " to all rolls."))


@bot.command(name='randchar')
async def random_char(ctx, boss=False):
    if boss:
        stat_cap = world["boss stat cap"]
    else:
        stat_cap = world["stat cap"]
    if world["number"] <= 0:
        await ctx.send("Invalid world.")
        return
    global next_backstory
    global next_short_name
    global next_name
    if next_backstory:
        backstory = next_backstory
        next_backstory = None
    else:
        backstory = random.choice(random_lists.Backstories)
    if next_short_name:
        first_name = next_short_name
        next_short_name = None
    else:
        first_name = random.choice(names.Names)
        while first_name in npcs.keys():
            first_name = random.choice(names.Names)
    if next_name:
        full_name = next_name
        next_name = None
    else:
        middle_name = None
        if random.randint(1, 2) == 2:
            middle_name = random.choice(names.Names)
        last_name = random.choice(names.Names)
        if middle_name:
            full_name = first_name + " " + middle_name + " " + last_name
        else:
            full_name = first_name + " " + last_name
    strongness = random.randint(0, stat_cap)
    smartness = random.randint(0, stat_cap)
    coolness = random.randint(0, stat_cap)
    health = 2 * strongness + 1
    gold = random.randint(0, stat_cap * 10)
    blessing_level = None
    blessing_roll = random.randint(1, 20)
    if blessing_roll <= world["number"]:
        blessing_level = "Level I"
        blessing_roll = random.randint(1, 20)
        if blessing_roll <= world["number"]:
            blessing_level = "Level II"
            blessing_roll = random.randint(1, 20)
            if blessing_roll <= world["number"]:
                blessing_level = "Level III"
    blessing_name = random.choice(random_lists.Blessings)
    if blessing_level is None:
        blessing = "No blessing"
    else:
        blessing = "**Blessing of " + blessing_name + "** " + blessing_level
    trait1 = random.choice(list(traits.trait_dict.keys()))
    trait2 = trait1
    while trait2 == trait1:
        trait2 = random.choice(list(traits.trait_dict.keys()))
    color_string = shared_functions.random_color()
    inventory = []
    for i in range(0, 3):
        if random.randint(1, 4) == 1:
            inventory.append((await items.random_item(ctx, -2 * world["number"], 1, False)).name)
        else:
            inventory.append("Empty slot")
    if boss:
        backstory = random.choice(random_lists.BossBackstories)
        trait1 = random.choice(list(traits.boss_trait_dict.keys()))
        health *= (5 * world["number"])
        gold *= (world["number"] * world["number"])
        full_name = "*Boss:* " + full_name
        secondary_trait_roll = random.randint(1, 20)
        if secondary_trait_roll <= world["number"]:
            trait2 = random.choice(traits.boss_trait_dict)
            while trait1 == trait2:
                trait2 = random.choice(traits.boss_trait_dict)
    character = {"Backstory": backstory, "Name": full_name, "Traits": [trait1, trait2], "Smartness": smartness,
                 "Coolness": coolness, "Strongness": strongness, "Health": health, "Gold": gold, "Color": color_string,
                 "Inventory": inventory, "Blessing": blessing}
    npcs[first_name] = character
    await ctx.send(embed=characters.print_character(first_name))
    shared_functions.backup_characters()


@bot.command(name='randboss')
async def random_boss(ctx):
    await random_char(ctx, True)


@bot.command(name='encounter')
async def encounter(ctx):
    world_number = world["number"]
    roll = random.randint(1, 99)
    if roll > 66:
        await randnpc(ctx)
    elif roll < world_number + 1:
        await random_boss(ctx)
    else:
        await random_char(ctx)


@bot.command(name="sell")
async def sell(ctx, character_name, item_name, show_price=False):
    # TODO: Add support to attempt to sell an item to an NPC.
    character = shared_functions.find_character(character_name)
    if not character:
        await ctx.send("No character named " + character_name)
        return
    if item_name not in items.item_dict.keys():
        await ctx.send("No item named " + item_name)
        return
    if item_name not in character["Inventory"]:
        await ctx.send(character_name + " does not have " + item_name + " in their inventory!")
        return
    item = items.item_dict[item_name]
    if item.quality == 0:
        price = 0
    elif item.quality == 1:
        price = 1
    elif item.quality == 2:
        price = 10
    elif item.quality == 3:
        price = 50
    elif item.quality == 4:
        price = 100
    elif item.quality == 5:
        price = 1000
    if show_price:
        await ctx.send("Selling this item will net you ", price, " gold.")
    else:
        character["Gold"] += price
        await remove_item(ctx, character_name, item_name)
    shared_functions.backup_characters()

    # Selling to NPC: Good roll: NPC will buy for close to full price if they have enough gold, and tell you 'I can't
    # afford that' otherwise. Bad roll: NPC will buy for low price close to store price. If NPC doesn't have enough
    # gold still, they will offer all their gold.


@bot.event
async def on_message(message):
    # Currently, if the bot is down, it will not check the channel history to see if it missed any inputs
    # while it was down. This is not too hard to do (save the message ID of the latest read message in the JSON,
    # then get history in this channel since that message and iterate through all missed messages on boot,
    # disregarding all but the first from each user).

    # If there is ever a need for message-by-message scanning, the wizard can be safely tucked into a function and left
    #  in wizards.py, with the actual event moved to main.

    if message.channel.id == 714589518983987212 or message.channel.id == 714628821646835889:
        await wizard.wizard_main(message)
    await bot.process_commands(message)


bot.run(TOKEN)
