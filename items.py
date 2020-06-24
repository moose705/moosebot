from bot import bot as bot
from shared_functions import world as world
# remove after roll is implemented separately
import random
import classes
import shared_functions
import characters

items = shared_functions.get_dict_from_json("items.json")

item_dict = {}
cursed_item_dict = {}
awful_item_dict = {}
meh_item_dict = {}
good_item_dict = {}
great_item_dict = {}
godly_item_dict = {}
item_dict_list = [cursed_item_dict, awful_item_dict, meh_item_dict, good_item_dict, great_item_dict, godly_item_dict]

for item in items.keys():
    item_dict[item] = classes.Item(item, items[item]["description"], items[item]["teaser"], items[item]["damage"],
                                   items[item]["quality"], items[item]["type"])
    item_dict_list[item_dict[item].quality][item] = item_dict[item]

# how many items per shop?
NUM_ITEMS = 5


@bot.command(name='randitem')
async def random_item(ctx, modifier=0, number=1, print_items=True):
    # TODO: Implement a global roll function
    return_list = []
    for i in range(0, number):
        modifier += world["modifier"]
        roll = random.randint(1, 20)
        if roll != 1 and roll != 20:
            roll += modifier
        if roll <= 1:
            chosen_item = random.choice(list(cursed_item_dict.values()))
        elif roll < 6:
            chosen_item = random.choice(list(awful_item_dict.values()))
        elif roll < 11:
            chosen_item = random.choice(list(meh_item_dict.values()))
        elif roll < 16:
            chosen_item = random.choice(list(good_item_dict.values()))
        elif roll < 20:
            chosen_item = random.choice(list(great_item_dict.values()))
        else:
            chosen_item = random.choice(list(godly_item_dict.values()))
        if print_items:
            await ctx.send(chosen_item.print_teaser())
        return_list.append(chosen_item)
    if len(return_list) == 1:
        return_list = return_list[0]
    return return_list


@bot.command(name='shop')
async def generate_shop(ctx):
    # TODO: Add Black Market, Trait-generated options as a parameter for shop

    # The black market shop will probably generate less items with a much more favorable modifier and reduced prices?

    # If we implement multiple shop types it may make sense to refactor this to use like a prices list.

    # Modifier in world 1 and 2: -4 (World mod: 1; thus, -5)
    # Modifier in world 3 and 4: -3 (World mod: 0, thus, -3)
    # Modifier in world 5 and 6: -2 (World mod, -1, thus, -1)
    # Modifier in world 7 and 8: -1 (World mod: -2, thus, +1)
    # Modifier in world 9 onwards: 0 (World mod: -3, thus, +3)
    shop_items = await random_item(ctx, 2 * int((world["number"] - 1) / 2) - 5, NUM_ITEMS, False)
    shop_list = []
    for shop_item in shop_items:
        if shop_item.quality == 0:
            price = random.randint(1, 10000)
        elif shop_item.quality == 1:
            price = random.randint(1, 100)
        elif shop_item.quality == 2:
            price = random.randint(100, 500)
        elif shop_item.quality == 3:
            price = random.randint(500, 1000)
        elif shop_item.quality == 4:
            price = random.randint(1000, 5000)
        elif shop_item.quality == 5:
            price = random.randint(10000, 50000)
        item_dict[shop_item.name].last_price = price
        shop_list.append((price, "***" + str(price) + " gold -*** " + shop_item.print_teaser()))
    shop_list = sorted(shop_list, key=lambda x: x[0])
    for price_and_item in shop_list:
        await ctx.send(price_and_item[1])

    # We can pass a modifier to randitem so use it that way.
    # Shop additionally needs to determine and print a price, though. It can do that by checking quality of its
    # desired item.


@bot.command(name="buy", aliases=["spend", "purchase"])
async def buy(ctx, name, item_name):
    if item_name not in item_dict.keys():
        await ctx.send("I've never heard of that item...")
        return
    gold = item_dict[item_name].last_price
    character = shared_functions.find_character(name)
    if not character:
        await ctx.send("Character " + name + " does not exist!")
        return
    if gold > int(character["Gold"]):
        await ctx.send("Not enough gold!")
        return
    for slot in character["Inventory"]:
        if slot == "Empty slot":
            slot_number = character["Inventory"].index(slot)
            break
    else:
        await ctx.send("Not enough inventory space!")
    character["Inventory"][slot_number] = item_name
    character["Gold"] = character["Gold"] - gold
    await ctx.send(embed=characters.print_character(name))


