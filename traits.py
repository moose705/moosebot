import shared_functions
import classes
import characters

from bot import bot as bot

traits = shared_functions.get_dict_from_json("traits.json")
blessings = shared_functions.get_dict_from_json("blessings.json")
boss_traits = shared_functions.get_dict_from_json("boss_traits.json")

trait_dict = {}
boss_trait_dict = {}
blessing_dict = {}

for trait in traits.keys():
    trait_dict[trait] = classes.Trait(trait, traits[trait])

for boss_trait in boss_traits.keys():
    boss_trait_dict[boss_trait] = classes.Trait(boss_trait, boss_traits[boss_trait])

for blessing in blessings.keys():
    # this is messy and needs testing
    # json could contain them in any order, so this attempts to link both ways
    blessing_dict[blessing] = classes.Trait(blessing, blessings[blessing])
    if blessing[-7:].lower() == "level i":
        for blessing_1 in blessing_dict.keys():
            if blessing_1.lower() == blessing[0:-7].lower() + "level ii":
                blessing_dict[blessing_1].downgrade = blessing
                blessing.upgrade = blessing_1
    if blessing[-8:].lower() == "level ii":
        for blessing_1 in blessing_dict.keys():
            if blessing_1.lower() == blessing[0:-7].lower() + "level i":
                blessing_dict[blessing_1].upgrade = blessing
                blessing.downgrade = blessing_1
        for blessing_1 in blessing_dict.keys():
            if blessing_1.lower() == blessing[0:-9].lower() + "level iii":
                blessing_dict[blessing_1].downgrade = blessing
                blessing.upgrade = blessing_1
    if blessing[-9:].lower() == "level iii":
        for blessing_1 in blessing_dict.keys():
            if blessing_1.lower() == blessing[0:-7].lower() + "level ii":
                blessing_dict[blessing_1].upgrade = blessing
                blessing.downgrade = blessing_1
    # TODO: Manage Unlocked status of a blessing. Bonus points if %win automatically unlocks god blessings

# These don't really belong in this module and they force me to import characters to print, but oh well.


@bot.command(name='changetrait')
async def change_trait(ctx, name, old_trait, new_trait):
    character = shared_functions.find_character(name)
    if not character:
        await ctx.send("Party member or NPC not found.")
        return
    if new_trait not in trait_dict:
        await ctx.send("Trait " + new_trait + " does not exist!")
        return
    if old_trait not in character["Traits"]:
        if old_trait == "1":
            old_trait = character["Traits"][0]
        elif old_trait == "2":
            old_trait = character["Traits"][1]
        elif old_trait == "3":
            old_trait = character["Traits"][2]
        else:
            await ctx.send("Character " + name + " does not have trait " + old_trait + "!")
            return
    character["Traits"][character["Traits"].index(old_trait)] = new_trait
    await ctx.send(embed=characters.print_character(name))


@bot.command(name='changeblessing')
async def change_blessing(ctx, name, blessing, override=False):
    character = shared_functions.find_character(name)
    if not character:
        await ctx.send("Character does not exist")
        return
    if blessing not in blessing_dict and override is not False:
        await ctx.send("Blessing does not exist or is not unlocked")
        return
    character["Blessing"] = blessing
    await ctx.send(embed=characters.print_character(name))
