import random
import shared_functions

from shared_functions import party as party
from bot import bot as bot

def stat_wizard(message, wizard_data):
    try:
        stat = int(message.content)
    except ValueError:
        return "That doesn't seem like a number buddy."
    if stat < 0:
        return "Negative stats aren't allowed at character creation; please submit a zero or positive number"
    if stat > 11:
        return "The three stats have to add up to 11. How are they supposed to do that if one of them is already\
         bigger than 11..."
    wizard_data[wizard_data["Phase"]] = stat
    if wizard_data["Phase"] == "Strongness":
        wizard_data["Phase"] = "Smartness"
    elif wizard_data["Phase"] == "Smartness":
        wizard_data["Phase"] = "Coolness"
    elif wizard_data["Phase"] == "Coolness":
        return ""
    return "What is your character's " + wizard_data["Phase"] + "?"


def trait_wizard(message, wizard_data):
    response = ""
    if wizard_data["Phase"] == "Coolness":
        filename = "traits.json"
        num_samples = 3
        option_string = "Trait Options"
        wizard_data["Phase"] = "Traits"
    else:
        option_string = wizard_data["Phase"] + " Options"
        if option_string == "Traits Options":
            option_string = "Trait Options"
        if message.content not in wizard_data[option_string]:
            return "Choice not recognized as one of the options. Make sure you sent it exactly as shown, I am just a " \
                   "stupid robot..."
        if wizard_data["Phase"] == "Traits":
            filename = "blessings.json"
            num_samples = 5
            option_string = "Blessing Options"
            wizard_data["Phase"] = "Blessing"
            options_dict = shared_functions.get_dict_from_json("traits.json")
            wizard_data["Traits"].append("** " + message.content + "**: " + options_dict[message.content])
        else:
            options_dict = shared_functions.get_dict_from_json("blessings.json")
            wizard_data["Blessing"] = "**Blessing of " + message.content + "**: " + options_dict[message.content]
            return None
    options_dict = shared_functions.get_dict_from_json(filename)
    options = random.sample(options_dict.keys(), num_samples)
    wizard_data[option_string] = options
    response += "Choose **one** of the below random options:\n"
    for i in range(0, num_samples):
        response += "** " + options[i] + "**: " + options_dict[options[i]] + "\n"
    return response


@bot.event
async def on_message(message):
    # The wizard is handled through this nightmare of an event.

    # Currently, if the bot is down, it will not check the channel history to see if it missed any wizard inputs
    # while it was down. This is not too hard to do (save the message ID of the latest read message in the JSON,
    # then get history in this channel since that message and iterate through all missed messages on boot,
    # disregarding all but the first from each user).

    wizards = shared_functions.get_dict_from_json("wizards.json")
    if message.author == bot.user:
        return
    if message.channel.id == 714589518983987212 or message.channel.id == 714628821646835889:
        user_discriminator = message.author.discriminator
        try:
            phase = wizards[user_discriminator]["Phase"]
        except KeyError:
            if message.content == "%wizard":
                ping = message.author.mention
                await message.channel.send("Character creation wizard activated for " + ping)
                wizards[user_discriminator] = {"Phase": "Long name"}
                await message.channel.send("What is your character's full name? (Spaces allowed)")
                shared_functions.backup_wizards(wizards)
            return
        wizard_data = wizards[user_discriminator]
        if phase == "Long name":
            wizard_data["Long name"] = message.content
            wizard_data["Short name"] = message.content.split(" ")[0]
            if shared_functions.find_character(wizard_data["Short name"]):
                await message.channel.send("Alas, a character already exists with the name of "
                                           + wizard_data["Short name"] + ". Please try again.")
                return
            wizard_data["Traits"] = []
            wizard_data["Phase"] = "Backstory"
            await message.channel.send("What is your character's backstory?")
        elif phase == "Backstory":
            wizard_data["Backstory"] = message.content
            wizard_data["Phase"] = "Strongness"
            await message.channel.send(
                "What is your character's Strongness? (There are 3 stats; they must add up to 11.)")
        elif phase == "Strongness":
            await message.channel.send(stat_wizard(message, wizard_data))
        elif phase == "Smartness":
            await message.channel.send(stat_wizard(message, wizard_data))
        elif phase == "Coolness":
            wizard_message = stat_wizard(message, wizard_data)
            if wizard_message:
                await message.channel.send(wizard_message)
            try:
                summ = wizard_data["Strongness"] + wizard_data["Smartness"] + wizard_data["Coolness"]
            except KeyError:
                shared_functions.backup_wizards(wizards)
                return
            if summ != 11:
                await message.channel.send("Is math not your strong suit...? Those numbers add up to " + str(
                    summ) + ", not 11!\n What is your character's Strongness?")
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
                await message.channel.send(trait_wizard(message, wizard_data))
        elif phase == "Traits":
            await message.channel.send(trait_wizard(message, wizard_data))
        elif phase == "Blessing":
            wizard_response = trait_wizard(message, wizard_data)
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
