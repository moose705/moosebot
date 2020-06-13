import json
import os
import random
import outcome_tables
import discord 
import random_lists
import names
import wizard
import sys

# below: laziness
from shared_functions import party as party
from shared_functions import npcs as npcs
from shared_functions import next_backstory as next_backstory
from shared_functions import next_name as next_name
from shared_functions import next_short_name as next_short_name

import shared_functions
import stat_commands
import old_commands
from bot import bot as bot
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
# Party & NPC Management

def add_character(name):
  party[name] = {}
  party[name]["Traits"] = []
  party[name]["Blessing"] = "None"
  party[name]["Inventory"] = ["Empty slot", "Empty slot", "Empty slot"]
 
def change_character_data(name, data, value):
  if data == "Strongness" or data == "Smartness" or data == "Coolness" or data == "Health" or data == "Gold":
    value = int(value) 
    # Hidden stats need handling here when implemented.

  character = shared_functions.find_character(name)
  if not character:
    return
  character[data] = value

def print_character(name, character=None):
  """Given the name of a character which is either in the party or npc dictionaries, returns an Embed object with all of their relevant qualities. 
  
  An optional character option can be used to override the function's attempts to search and pass this function the dictionary."""
  if not character:
    character = shared_functions.find_character(name)
    if not character:
      return discord.Embed(title="Invalid character")
  embed = discord.Embed(title=character["Name"], description=character["Backstory"], color=int(character["Color"], 16))
  embed.add_field(name="**Strongness**", value= character["Strongness"])
  embed.add_field(name="**Smartness**", value = character["Smartness"])
  embed.add_field(name="**Coolness**", value = character["Coolness"])
  embed.add_field(name="**Health**", value=character["Health"])
  embed.add_field(name="**Gold**", value=character["Gold"])
  embed.add_field(name="__**Traits**__", value = character["Traits"][0] + "\n" + character["Traits"][1])
  embed.add_field(name="__**Blessing**__", value=character["Blessing"])
  inventory_string = ""
  for item in character["Inventory"]:
    inventory_string += "- " + item + "\n"
  embed.add_field(name="__**Inventory**__", value=inventory_string)
  shared_functions.backup_characters() 
  return embed

@bot.command(name='addchar')
async def add_char(ctx, shortname, name, backstory=None, health=None, gold=None, strongness=None, smartness=None, coolness=None, trait1=None, trait2=None, blessing=None, inventory1=None, inventory2=None, inventory3=None):
  name = name.replace("±", " ")
  add_character(shortname)
  change_character_data(shortname, "Name", name)
  name = shortname
  if backstory:
    backstory = backstory.replace("±", " ")
    change_character_data(name, "Backstory", backstory)
  if health:
    change_character_data(name, "Health", health)
  if gold:
    change_character_data(name, "Gold", gold)
  if strongness:
    change_character_data(name, "Strongness", strongness)
  if smartness:
    change_character_data(name, "Smartness", smartness)
  if coolness:
    change_character_data(name, "Coolness", coolness)
  if trait1:
    trait1 = trait1.replace("±", " ")
    party[name]["Traits"].append(trait1)
  if trait2:
    trait2 = trait2.replace("±", " ")
    party[name]["Traits"].append(trait2)
  if blessing: 
    blessing = blessing.replace("±", " ")
    party[name]["Blessing"] = blessing
  if inventory1:
    inventory1 = inventory1.replace("±", " ")
    party[name]["Inventory"][0] = inventory1
  if inventory2:
    inventory2 = inventory2.replace("±", " ")
    party[name]["Inventory"][1] = inventory2
  if inventory3:
    inventory3 = inventory3.replace("±", " ")
    party[name]["Inventory"][2] = inventory3
  party[name]["Color"] = shared_functions.random_color()
  response = 'Successfully added character'
  shared_functions.backup_characters()
  await ctx.send(response)
 
@bot.command(name='changechar')
async def change_char(ctx, name, quality, value):
  value = value.replace("±", " ")
  change_character_data(name, quality, value)
  response = print_character(name)
  await ctx.send(embed=response)

@bot.command(name='changetrait')
async def change_trait(ctx, name, old_trait, new_trait):
  character = shared_functions.find_character(name)
  if not character:
    await ctx.send("Party member or NPC not found.")
    return
  existing_traits = []
  for trait in character["Traits"]:
    existing_traits.append(trait.split(":")[0].replace(" ", "").replace("*", ""))
  if old_trait not in existing_traits:
    await ctx.send("Character does not have specified trait to replace.")
    return
  traits_json = open("traits.json", "r")
  traits_json_string = traits_json.read()
  traits_dict = json.loads(traits_json_string)
  traits_json.close()
  try:
    traits_dict[new_trait]
  except KeyError:
    await ctx.send("Trait " + new_trait + " does not exist!")
    return 
  index_to_replace = existing_traits.index(old_trait)
  character["Traits"][index_to_replace] = "**" + new_trait + "**: " + traits_dict[new_trait]
  await ctx.send(embed=print_character(name))
    
@bot.command(name='countitems')
async def count_items(ctx):
  num_items = len(random_lists.GoodItems) + len(random_lists.GodlyItems) + len(random_lists.GreatItems)+ len(random_lists.MehItems) + len(random_lists.AwfulItems) + len(random_lists.CursedItems)
  await ctx.send("There are " + str(num_items) + " items currently in the item pool.")

@bot.command(name='countbackstories')
async def count_backstories(ctx):
  num_backstories = len(random_lists.Backstories)
  await ctx.send("There are " + str(num_backstories) + " backstories currently in the backstory pool.")

@bot.command(name='nextname')
async def next_name_function(ctx, name):
  global next_short_name
  global next_name
  next_short_name = name.split(" ")[0]
  next_name = name

@bot.command(name='nextbackstory')
async def next_backstory_function(ctx, backstory):
  global next_backstory
  next_backstory = backstory
  
@bot.command(name='changeblessing')
async def change_blessing(ctx, name, blessing):
  blessing = blessing.replace("±", " ")
  blessings_dict = shared_functions.get_dict_from_json("blessings.json")
  character = shared_functions.find_character(name)
  if not character:
    await ctx.send("Character does not exist")
    return
  if blessing not in blessings_dict:
    await ctx.send("Blessing does not exist or is not unlocked")
    return
  character["Blessing"] = "**Blessing of " + blessing + "**: " + blessings_dict[blessing]
  await ctx.send(embed=print_character(name))

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
  await ctx.send(embed=print_character(name))

@bot.command(name='removeitem', aliases=["take", "drop"])
async def add_item(ctx, name, item):
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
  await ctx.send(embed=print_character(name))

@bot.command(name='buy', aliases=["spend", "purchase"])
async def buy(ctx, name, gold):
  gold = int(gold)
  character = shared_functions.find_character(name)
  if not character:
    await ctx.send("Character " + name + " does not exist!")
    return
  if gold > int(character["Gold"]):
    await ctx.send("Not enough gold!")
    return 
  character["Gold"] = str(int(character["Gold"]) - gold)
  await ctx.send(embed=print_character(name))

@bot.command(name='pay', aliases=["givemoney", "givegold"])
async def pay(ctx, name, gold):
  await buy(ctx, name, -int(gold))

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
  await ctx.send(embed=print_character(name))

@bot.command(name='decrease', aliases=["lowerstat", "decreasestat", "lower"])
async def decrease(ctx, name, stat, number):
  await increase(ctx, name, stat, -int(number))

@bot.command(name='damage', aliases=["hurt"])
async def damage(ctx, name, number):
  await decrease(ctx, name, "Health", number)
  character = shared_functions.find_character(name)
  if character and character["Health"] < 0:
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
    # hardcoded max health right now; will eventually need to change to a character["Max Health"] attribute if i implement things like Blessing of Bloat
    change_character_data(name, "Health", 2 * character["Strongness"] + 1)
    await ctx.send(embed=print_character(name))

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
  roll = random.randint(1,20)
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
  if not character:
    await ctx.send("No character named " + name)
    return
  if stat not in character:
    await ctx.send("Invalid stat")
    return
  roll = random.randint(1,20)
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
 
@bot.command(name='addchartrait', aliases=["addtrait", "givetrait"])
async def add_trait_to_char(ctx, name, trait):
  # Only the first two traits will be printed
  # This is a really useless command
  character = shared_functions.find_character(name)
  if not character:
    await ctx.send("Character does not exist.")
  character["Traits"].append(trait)
  response = print_character(name)
  await ctx.send(embed=response)
 
@bot.command(name='killchar', aliases=["kill", "nuke"])
async def kill_char(ctx, name):
  # Can't refactor this to use shared_functions.find_character because I need to know which dictionary to pop from 
  try:
    is_npc = False
    dead_guy_name = party[name]["Name"]
  except KeyError:
    try:
      dead_guy_name = npcs[name]["Name"]
      is_npc = True
    except KeyError:
      await ctx.send("Could not find party member or NPC named " + name)
  if not is_npc and party.pop(name, False):
    response = "**" + dead_guy_name + " has been slain.**"
  elif is_npc and npcs.pop(name, False):
    response = "**" + dead_guy_name + " has been slain.**"
  else:
    response = "Could not find character"
  shared_functions.backup_characters()
  await ctx.send(response)
 
@bot.command(name='party')
async def print_party(ctx, name=None):
  if not name:
    for character_name in party.keys():
      response = print_character(character_name)
      await ctx.send(embed=response)
  else:
    response = print_character(name)
    await ctx.send(embed=response)

@bot.command(name='npc')
async def npc(ctx, name=None):
  if not name:
    length = str(len(npcs.keys()))
    await ctx.send("There are currently " + length + " NPCs in the pool.")
    return
  await ctx.send(embed=print_character(name))

@bot.command(name='randnpc')
async def randnpc(ctx):
  if len(npcs.keys()) == 0:
    await ctx.send("There are no NPCs!")
    return
  npc = random.choice(list(npcs.keys()))
  await ctx.send(embed=print_character(npc))

@bot.command(name='recruit', aliases=["hire", "addparty"])
async def recruit(ctx, name):
  npc = npcs[name]
  npcs.pop(name)
  party[name] = npc
  shared_functions.backup_characters()
  await ctx.send(name + " added to party!")

@bot.command(name='fire', aliases=['retire', 'kick', 'ditch'])
async def leave(ctx,name):
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

@bot.command(name='retireparty')
async def retire_party(ctx):
  for name in list(party.keys()):
    await leave(ctx, name)
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
  await ctx.send(embed=print_character(name))

@bot.command(name='randitem')
async def random_item(ctx, modifier=0, number=1):
  for i in range(0, number):
    roll = random.randint(1, 20)
    if roll != 1 and roll != 20:
      roll += modifier
    if roll <= 1:
      await ctx.send(random.choice(random_lists.CursedItems))
    elif roll < 6:
      await ctx.send(random.choice(random_lists.AwfulItems))
    elif roll < 11:
      await ctx.send(random.choice(random_lists.MehItems))
    elif roll < 16:
      await ctx.send(random.choice(random_lists.GoodItems))
    elif roll < 20:
      await ctx.send(random.choice(random_lists.GreatItems))
    else:
      await ctx.send(random.choice(random_lists.GodlyItems))

@bot.command(name='restart')
async def restart(ctx):
    sys.exit()

@bot.command(name='randchar')
async def random_char(ctx, world=1, boss=False):
  if world <= 0:
    # underworld
    await ctx.send("Invalid world.")
    return
  stat_cap = world + 4
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
  while first_name in npcs:
    # should have above ~10 lines in a while loop forcing regeneration of duplicate names
    first_name = random.choice(names.Names)
  if next_name:
    full_name = next_name
    next_name = None
  else:
    middle_name = None
    if random.randint(1,2) == 2:
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
  blessing_roll = random.randint(1,20)
  if blessing_roll <= world:
    blessing_level = "Level I"
    blessing_roll = random.randint(1,20)
    if blessing_roll <= world:
      blessing_level = "Level II"
      blessing_roll = random.randint(1,20)
      if blessing_roll <= world:
        blessing_level = "Level III"
  blessing_name = random.choice(random_lists.Blessings)
  if blessing_level is None:
    blessing = "No blessing"
  else:
    blessing = "**Blessing of " + blessing_name + "** " + blessing_level
  traits_json = open("traits.json", "r")
  traits_json_string = traits_json.read()
  traits_json.close()
  traits_dict = json.loads(traits_json_string)
  trait1 = random.choice(list(traits_dict.keys()))
  trait2 = trait1
  while trait2 == trait1:
    trait2 = random.choice(list(traits_dict.keys()))
  trait1 = "**" + trait1 + "**: " + traits_dict[trait1]
  trait2 = "**" + trait2 + "**: " + traits_dict[trait2]
  color_string = shared_functions.random_color()
  inventory = []
  for i in range(0, 3):
    if random.randint(1,4) == 1:
      inventory.append("????")
    else:
      inventory.append("Empty slot")
  if boss:
    backstory = random.choice(random_lists.BossBackstories)
    trait1 = random.choice(random_lists.BossTraits)
    health *= (5 * world)
    gold *= (world * world)
    full_name = "*Boss:* " + full_name
    for stat in [strongness, smartness, coolness]:
      stat += random.randint(0,2)
    secondary_trait_roll = random.randint(1,20)
    if secondary_trait_roll <= world:
      trait2 = random.choice(random_lists.BossTraits)
      while trait1 == trait2:
        trait2 = random.choice(random_lists.BossTraits)
  character = {"Backstory": backstory, "Name": full_name, "Traits" : [trait1, trait2], "Smartness": smartness, "Coolness": coolness, "Strongness": strongness, "Health": health, "Gold": gold, "Color": color_string, "Inventory": inventory, "Blessing": blessing}
  await ctx.send(embed=print_character(first_name, character))
  npcs[first_name] = character
  shared_functions.backup_characters()

@bot.command(name='randboss')
async def random_boss(ctx, world=1):
  await random_char(ctx, world, True)

@bot.event
async def on_message(message):
  # The wizard is handled through this nightmare of an event.
  
  # Currently, if the bot is down, it will not check the channel history to see if it missed any wizard inputs while it was down. This is not too hard to do (save the message ID of the latest read message in the JSON, then get history in this channel since that message and iterate through all missed messages on boot, disregarding all but the first from each user).

  wizards = shared_functions.get_dict_from_json("wizards.json")
  if message.author == bot.user:
      return
  if message.channel.id == (714589518983987212) or message.channel.id == (714628821646835889):
      user_discriminator = message.author.discriminator
      try:
        print(user_discriminator)
        phase = wizards[user_discriminator]["Phase"]
      except KeyError:
        if message.content == "%wizard":
          ping = message.author.mention
          await message.channel.send("Character creation wizard activated for " + ping)
          wizards[user_discriminator] = {"Phase" : "Short name"}
          await message.channel.send("What is your character's first name? (No spaces plz, I am a stupid robot and will have a mental breakdown)")
          shared_functions.backup_wizards(wizards)
        return
      wizard_data = wizards[user_discriminator]
      if phase == "Short name":
        if " " in message.content:
          await message.channel.send("I said no spaces! How hard is it to follow basic instructions?")
        else:
          wizard_data["Short name"] = message.content
          wizard_data["Phase"] = "Long name"
          wizard_data["Traits"] = []
          await message.channel.send("What is your character's full name? (Spaces allowed)")
      elif phase == "Long name":
        wizard_data["Long name"] = message.content
        wizard_data["Phase"] = "Backstory"
        await message.channel.send("What is your character's backstory?")
      elif phase == "Backstory":
        wizard_data["Backstory"] = message.content
        wizard_data["Phase"] = "Strongness"
        await message.channel.send("What is your character's Strongness? (There are 3 stats; they must add up to 11.)")
      elif phase == "Strongness":
        await message.channel.send(wizard.stat_wizard(message, wizard_data))
      elif phase == "Smartness":
        await message.channel.send(wizard.stat_wizard(message, wizard_data))
      elif phase == "Coolness":
        wizard_message = wizard.stat_wizard(message, wizard_data)
        if wizard_message:
          await message.channel.send(wizard_message)
        try:
          summ = wizard_data["Strongness"] + wizard_data["Smartness"] + wizard_data["Coolness"]
        except KeyError:
          shared_functions.backup_wizards(wizards)
          return
        if summ != 11:
          await message.channel.send("Is math not your strong suit...? Those numbers add up to " + str(summ) + ", not 11!\n What is your character's Strongness?")
          wizard_data["Phase"] = "Strongness"
          wizard_data.pop("Coolness")
        else:
          starting_gold = random.randint(0, 100)
          await message.channel.send("Your character will start with " + str(starting_gold) + " Gold.")
          wizard_data["Gold"] = starting_gold
          wizard_data["Health"] = wizard_data["Strongness"] * 2 + 1
          trait_dict = shared_functions.get_dict_from_json("traits.json")
          random_trait = random.choice(list(trait_dict.keys()))
          random_trait_string = "** " + random_trait + "**: " + trait_dict[random_trait]
          wizard_data["Traits"].append(random_trait_string)
          await message.channel.send(wizard.trait_wizard(message, wizard_data))
      elif phase == "Traits":
        await message.channel.send(wizard.trait_wizard(message, wizard_data))
      elif phase == "Blessing":
        wizard_response = wizard.trait_wizard(message, wizard_data)
        if wizard_response:
          await message.channel.send(wizard_response)
          shared_functions.backup_wizards(wizards)
          return 
        await message.channel.send("Character creation wizard complete. Adding character to the party.")
        character_dict = {"Name": wizard_data["Long name"],
           "Strongness": wizard_data["Strongness"], 
           "Coolness": wizard_data["Coolness"],
           "Smartness": wizard_data["Smartness"], 
           "Traits": wizard_data["Traits"],
           "Inventory": ["Empty Slot", "Empty Slot", "Empty Slot"],
           "Blessing": wizard_data["Blessing"],
           "Color": shared_functions.random_color(),
          "Health": wizard_data["Health"],
          "Gold": wizard_data["Gold"],
          "Backstory": wizard_data["Backstory"]}
        party[wizard_data["Short name"]] = character_dict
        shared_functions.backup_characters()
        wizards.pop(user_discriminator)
  shared_functions.backup_wizards(wizards)
  await bot.process_commands(message)

bot.run(TOKEN)
