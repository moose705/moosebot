import shared_functions
import items
import discord

from shared_functions import party as party
from shared_functions import npcs as npcs
from shared_functions import world as world

from bot import bot as bot
from discord.ext import commands

# TODO: Think a little bit on a way to clean up imports.
#  For example, characters imports items and items imports characters.


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
    embed = discord.Embed(title=character["Name"], description=character["Backstory"],
                          color=int(character["Color"], 16))
    embed.add_field(name="**Strongness**", value=character["Strongness"])
    embed.add_field(name="**Smartness**", value=character["Smartness"])
    embed.add_field(name="**Coolness**", value=character["Coolness"])
    embed.add_field(name="**Health**", value=character["Health"])
    embed.add_field(name="**Gold**", value=character["Gold"])
    # TODO: When printing traits, use the trait method
    # TODO: Add support for third trait
    embed.add_field(name="__**Traits**__", value=character["Traits"][0] + "\n" + character["Traits"][1])
    embed.add_field(name="__**Blessing**__", value=character["Blessing"])
    inventory_string = ""
    # TODO: If character is an NPC, hide their inventory unless an item is revealed. Need an NPC attribute.
    # this can be done i think by adding a "Hidden" attribute to the item class, and making it default on NPCs
    for item in character["Inventory"]:
        if item != "Empty slot":
            item = items.item_dict[item]
            inventory_string += "- " + item.print() + "\n"
        else:
            inventory_string += "- Empty slot\n"
    embed.add_field(name="__**Inventory**__", value=inventory_string)
    shared_functions.backup_characters()
    return embed


@bot.command(name='changechar')
async def change_char(ctx, name, quality, value):
    # TODO: Call changetrait for Trait1, Trait2, Trait3, Blessing
    # TODO: Print an error message if you try to change item or inventory
    value = value.replace("±", " ")
    change_character_data(name, quality, value)
    response = print_character(name)
    await ctx.send(embed=response)


@bot.command(name='changetrait')
async def change_trait(ctx, name, old_trait, new_trait):
    # TODO: Reformat to work with the new trait class dictionary, removing old trait functionality
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
    traits_dict = shared_functions.get_dict_from_json("traits.json")
    try:
        traits_dict[new_trait]
    except KeyError:
        await ctx.send("Trait " + new_trait + " does not exist!")
        return
    index_to_replace = existing_traits.index(old_trait)
    character["Traits"][index_to_replace] = "**" + new_trait + "**: " + traits_dict[new_trait]
    await ctx.send(embed=print_character(name))
