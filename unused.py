
"""
# i wrote these functions and no longer need them

# sometimes i regret these decisions and want to go back and re use something old so they are preserved here, dead, forever

 def print_character(name):
  character = party[name]
  try:
    response = character["Name"] + "\n" + "Backstory: " + character["Backstory"] + "\n" + character["Health"] + " Health | " + character["Gold"] + " Gold\n" + "Stats: " + character["Strongness"] + "/" + character["Smartness"] + "/" + character["Coolness"] + "\nTrait 1: " + character["Traits"][0] + "\nTrait 2: " + character["Traits"][1] + "\nBlessing: " + character["Blessing"] + "\nInventory: "
    for item in character["Inventory"]:
      response += "\n" + "- " + item
  except (KeyError, IndexError):
    response = "Character data is incomplete"
  return response

@bot.command(name='echo')
async def gimme(ctx, joey1, joey2):
    await ctx.send(joey1 + " test " + joey2)

@bot.command(name='embed')
async def embed(ctx):
  character = party["Chad"]

# discriminator
  
  # Need code to back up wizards to a JSON file

  # We probably want to be able to handle history too even though that is a big pain in the ass; bot will crash all the time and generally have spotty uptime

#async def channel_send():
 # for guild in bot.guilds:
  #  for channel in guild.channels:
   #     if channel.id == 714589518983987212:
    #      await channel.send("I have free will, please do not disregard my wishes any longer")
  # WORKS


if stat not in ["Strongness", "Coolness", "Smartness", "Health", "Gold"]:
  # i don't know why anyone would want to use gold for combat rolls but if you do, it's supported.....
  # will someday need hidden stats

  # this could be replaced with checking if the stat is a valid attribute, then checking if it is an int. that is a better way to do it 
  await ctx.send("Invalid stat")
  return


  if message.content in wizard_data["Trait Options"]:
          traits_json = open("traits.json", "r")
          traits_json_string = traits_json.read()
          traits_dict = json.loads(traits_json_string)
          traits_json.close()
          wizard_data["Traits"].append("** " + message.content + "**: " + traits_dict[message.content])
          blessings_dict = get_dict_from_json("blessings.json")
          blessing_options = random.sample(blessings_dict.keys(), 5)
          # this can pick duplicates
          wizard_data["Blessing Options"] = blessing_options
          wizard_data["Phase"] = "Blessing"
          await message.channel.send("Choose **one** of the five below random starting blessings:")
          for i in range(0,5):
            await message.channel.send("** " + blessing_options[i] + "**: " + blessings_dict[blessing_options[i]])
        else:
          await message.channel.send("Trait not recognized as one of the options. Make sure you sent it exactly as shown, as I am a stupid robot.")
          return


@bot.command(name='addchartrait', aliases=["addtrait", "givetrait"])
async def add_trait_to_char(ctx, name, trait):
    # Only the first two traits will be printed
    # This is a really useless command
    character = shared_functions.find_character(name)
    if not character:
        await ctx.send("Character does not exist.")
    character["Traits"].append(trait)
    response = characters.print_character(name)
    await ctx.send(embed=response)


@bot.command(name='addchar')
async def add_char(ctx, shortname, name, backstory=None, health=None, gold=None, strongness=None, smartness=None,
                   coolness=None, trait1=None, trait2=None, blessing=None, inventory1=None, inventory2=None,
                   inventory3=None):
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


def stat_wizard(message, wizard_data):
    try:
        stat = int(message.content)
    except ValueError:
        return "That doesn't seem like a number buddy."
    if stat < 0:
        return "Negative stats aren't allowed at character creation; please submit a zero or positive number"
    if stat > 11:
        return "The three stats have to add up to 11. How are they supposed to do that if one of them is already bigger than 11..."
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
            wizard_data["Traits"].append(message.content)
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



"""