@bot.command(name='roll')
async def roll(ctx, roll_type="action", number=1, placeholder="d", sides=20, modifier=0):
  # broken 
    if number <= 0 or number > 10:
        await ctx.send("Please enter a number of dice between 1 and 10.")
        return
    if sides < 1:
        await ctx.send("Please enter a valid number of dice sides.")
        return
    
    response = ""
    if sides != 20:
        for i in range(0, number):
            response += f"Your roll: {random.randint(1, sides)}\n\n"
    else:
        for i in range(0, number):
            mod_int = int(modifier)
            raw_roll = random.randint(1,sides)
            modified_roll = raw_roll
            if raw_roll != 1 and raw_roll != 20:
                modified_roll += mod_int
                if modified_roll > 20:
                    modified_roll = 20
                if modified_roll < 1:
                    modified_roll = 1
                response += f"Your roll: {raw_roll}\n Modified roll: {raw_roll} + {mod_int} = {modified_roll}\n"
            else:
                response += f"Your roll: Natural {raw_roll}\n"
            if roll_type.lower() == "action":
                response += outcome_tables.action_outcomes(modified_roll)+"\n\n"
            elif roll_type.lower() == "combat":
                response += outcome_tables.combat_outcomes(modified_roll)+"\n\n"
            elif roll_type.lower() == "item":
                response += outcome_tables.item_outcomes(modified_roll)+"\n\n"
            else:
                response += ("Invalid roll type" + raw_roll) + modified_roll
    await ctx.send(response)

# This works but it is missing all the new commands 

@bot.command(name='commands')
async def commands(ctx):
    #deprecated
    inforandt = "```$randtrait``` to get a random trait from our list,\n"
    infofind = "```$find \"Name of trait in quotes\" ``` to find a trait in the list and have me define it, \n"
    infoins = "```$insert \"Name of trait in quotes\" \"Definition of trait in quotes\"``` to insert a new trait and definition in our traits file,"
    infodel = "```$delete \"Name of trait in quotes\" ``` to delete a trait if it is in our traits file,\n"
    infogimme = "```$gimme``` to get the file of traits in chat, \n"
    infochar = "``` $charactertraits``` to get a list of traits to choose from and one which you are stuck with,\n"
    inforoll = "``` $roll [type \"action\"\"combat\"\"item\"] [number of dice to roll] [\"d\"][sides of dice] [modifier]``` to roll for an outcome of the three types, and how many dice you want to roll. Defaults to action roll of 1d20 with modifier 0."
    message = f'Type {inforandt}{infofind}{infoins}{infodel}{infogimme}{infochar}{inforoll}'
    await ctx.send(message)
 
