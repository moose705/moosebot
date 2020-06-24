import random
import shared_functions
import traits
import items

from shared_functions import party as party
from bot import bot as bot


async def get_user_data(wizards, message):
    user_discriminator = message.author.discriminator
    try:
        wizards[user_discriminator]["Phase"]
        wizards[user_discriminator]["Discriminator"] = user_discriminator
        return wizards[user_discriminator]
    except KeyError:
        if message.content == "%wizard" or message.content == "wizard":
            ping = message.author.mention
            await message.channel.send("Character creation wizard activated for " + ping)
            wizards[user_discriminator] = {"Phase": "Long name"}
            await message.channel.send("What is your character's full name? (Spaces allowed)")
            shared_functions.backup_wizards(wizards)
        return


async def check_numerical(message):
    try:
        stat = int(message.content)
    except ValueError:
        await message.channel.send("That doesn't seem like a number buddy.")
        return False
    if stat < 0:
        await message.channel.send("Negative stats aren't allowed at character creation; please submit a zero or "
                                   "positive number")
        return False
    if stat > 11:
        await message.channel.send("The three stats have to add up to 11. How are they supposed to do that if one of" +
                                   "them is already bigger than 11...")
        return False
    return True


async def assign_options(dictionary, num_options, message, item=False):
    bot_message = ""
    options_list = random.sample(list(dictionary.keys()), num_options)
    bot_message += ("Choose one of the following " + str(num_options) + " random options. \n")
    for option in options_list:
        if item:
            bot_message += dictionary[option].print_teaser() + "\n"
        else:
            bot_message += dictionary[option].print() + "\n"
    if item:
        bot_message += "A stat point can be exchanged to re-roll the given items. To do so, respond with a stat to " \
                       "exchange. "
    await message.channel.send(bot_message)
    return options_list


async def check_if_valid_option(options, message):
    if message.content not in options:
        option_string = ""
        for option in options:
            if option == options[-1]:
                option_string += "and " + option + "."
            else:
                option_string += option + ", "
        await message.channel.send("That was not a valid option. The options were: " + option_string)
        return False
    return True


async def wizard_main(message):
    wizards = shared_functions.get_dict_from_json("wizards.json")
    wizard_data = await get_user_data(wizards, message)
    if not wizard_data:
        return
    phase = wizard_data["Phase"]
    if phase == "Long name":
        wizard_data["Short name"] = message.content.split(" ")[0]
        if shared_functions.find_character(wizard_data["Short name"]):
            await message.channel.send("Alas, a character already exists with the name of "
                                       + wizard_data["Short name"] + ". Please try again.")
            return
        wizard_data["Long name"] = message.content
        wizard_data["Traits"] = []
        wizard_data["Phase"] = "Backstory"
        await message.channel.send("What is your character's backstory?")
    elif phase == "Backstory":
        wizard_data["Backstory"] = message.content
        wizard_data["Phase"] = "Strongness"
        await message.channel.send(
            "What is your character's Strongness? (There are 3 stats; they must add up to 11.)")
    elif phase == "Strongness":
        if await check_numerical(message):
            wizard_data["Strongness"] = int(message.content)
            wizard_data["Phase"] = "Smartness"
            await message.channel.send("What is your character's Smartness?")
    elif phase == "Smartness":
        if await check_numerical(message):
            wizard_data["Smartness"] = int(message.content)
            wizard_data["Phase"] = "Coolness"
            await message.channel.send("What is your character's Coolness?")
    elif phase == "Coolness":
        if await check_numerical(message):
            wizard_data["Coolness"] = int(message.content)
        stat_total = wizard_data["Strongness"] + wizard_data["Smartness"] + wizard_data["Coolness"]
        if stat_total != 11:
            await message.channel.send("Is math not your strong suit...? Those numbers add up to " + str(
                stat_total) + ", not 11!\n What is your character's Strongness?")
            wizard_data["Phase"] = "Strongness"
        else:
            starting_gold = random.randint(0, 100)
            await message.channel.send("Your character will start with " + str(starting_gold) + " Gold.")
            wizard_data["Gold"] = starting_gold
            wizard_data["Health"] = wizard_data["Strongness"] * 2 + 1
            wizard_data["Traits"].append(random.choice(list(traits.trait_dict.keys())))
            await message.channel.send("Your random trait is: " +
                                       traits.trait_dict[wizard_data["Traits"][0]].print())
            wizard_data["Options"] = await assign_options(traits.trait_dict, 3, message)
            wizard_data["Phase"] = "Traits"
    elif phase == "Traits":
        if await check_if_valid_option(wizard_data["Options"], message):
            wizard_data["Traits"].append(message.content)
            wizard_data["Options"] = await assign_options(traits.blessing_dict, 5, message)
            wizard_data["Phase"] = "Blessing"
    elif phase == "Blessing":
        if await check_if_valid_option(wizard_data["Options"], message):
            wizard_data["Blessing"] = message.content
            wizard_data["Options"] = await assign_options(items.item_dict, 3, message, True)
            # TODO: Instead of giving completely random items, give items based on a roll.
            #  This probably involves an actual roll refactor, which would make sense ASAP.
            #  I don't love the way world is currently implemented, particularly in relation to the wizard.
            wizard_data["Phase"] = "Item"
    elif phase == "Item":
        if message.content in ["Strongness", "Smartness", "Coolness"]:
            if wizard_data[message.content] > 0:
                wizard_data[message.content] -= 1
                wizard_data["Options"] = await assign_options(items.item_dict, 3, message, True)
            else:
                await message.channel.send("You don't have any more " + message.content + " to gamble!")
        elif await check_if_valid_option(wizard_data["Options"], message):
            wizard_data["Inventory"] = [message.content, "Empty slot", "Empty slot"]
            await message.channel.send("Character creation wizard complete. Adding character to the party.")
            character_dict = {"Name": wizard_data["Long name"],
                              "Strongness": wizard_data["Strongness"],
                              "Coolness": wizard_data["Coolness"],
                              "Smartness": wizard_data["Smartness"],
                              "Traits": wizard_data["Traits"],
                              "Inventory": wizard_data["Inventory"],
                              "Blessing": wizard_data["Blessing"],
                              "Color": shared_functions.random_color(),
                              "Health": wizard_data["Health"],
                              "Gold": wizard_data["Gold"],
                              "Backstory": wizard_data["Backstory"]}
            party[wizard_data["Short name"]] = character_dict
            shared_functions.backup_characters()
            wizards.pop(wizard_data["Discriminator"])

    shared_functions.backup_wizards(wizards)

