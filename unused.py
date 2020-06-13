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