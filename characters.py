import shared_functions
import items
import traits
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


def print_character(name):
    """Given the name of a character which is either in the party or npc dictionaries, returns an Embed object with all of their relevant qualities."""
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
    traits_field = ""
    for trait in character["Traits"]:
        try:
            traits_field += traits.trait_dict[trait].print() + "\n"
        except KeyError:
            traits_field += traits.boss_trait_dict[trait].print() + "\n"
    embed.add_field(name="__**Traits**__", value=traits_field)
    # TODO: Implement support in print_character for blessings that aren't unlocked.
    #  None are currently implemented, so it can wait.
    if character["Blessing"] in traits.blessing_dict:
        embed.add_field(name="__**Blessing**__", value=traits.blessing_dict[character["Blessing"]].print())
    else:
        if character["Blessing"] != "No blessing":
            embed.add_field(name="__**Blessing**__", value="**" + character["Blessing"] + "**: ????")
    inventory_string = ""
    for item in character["Inventory"]:
        if item != "Empty slot":
            if name in npcs.keys():
                inventory_string += "**Unknown item**: ???\n"
            else:
                item = items.item_dict[item]
                inventory_string += "- " + item.print() + "\n"
        else:
            inventory_string += "- Empty slot\n"
    embed.add_field(name="__**Inventory**__", value=inventory_string)
    shared_functions.backup_characters()
    return embed


@bot.command(name='changechar')
async def change_char(ctx, name, quality, value):
    value = value.replace("±", " ")
    if quality in ["Traits", "Blessing", "Inventory"]:
        await ctx.send("You're using the wrong command for this (try %changetrait, %changeblessing, %additem, "
                       "%removeitem)")
        return
    change_character_data(name, quality, value)
    response = print_character(name)
    await ctx.send(embed=response)
