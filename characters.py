import shared_functions
import stat_commands
import discord

from shared_functions import party as party
from shared_functions import npcs as npcs
from shared_functions import world as world

from bot import bot as bot
from discord.ext import commands

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

