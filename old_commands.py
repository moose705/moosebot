# These are really outdated, almost nothing has been changed since the old implementation. For example they still work with traits.txt, not traits.json. 

from bot import bot as bot
import random

@bot.command(name='randtrait')
async def random_trait(ctx):
    opened = open("traits.txt", "r")
    traits = [line for line in opened]
    numlines = len(traits)
    response = traits[random.randint(0, numlines-1)]
    await ctx.send(response)

@bot.command(name='charactertraits')
async def charater_traits(ctx):
    opened = open("traits.txt", "r")
    traits = [line for line in opened]
    numlines = len(traits)
    random_numbers=random.sample(range(numlines), 4)
    response = "*Trait 1: select **one** of the three following random traits:* \n" 
    response += traits[random_numbers[0]]
    response += traits[random_numbers[1]]
    response += traits[random_numbers[2]]
    response += "\n*Trait 2: Your character is stuck with this trait.*\n" 
    response += traits[random_numbers[3]]
    await ctx.send(response)

@bot.command(name='find')
async def search(ctx, arg):
    opened = open("traits.txt", "r")
    traits = [line for line in opened]
    for line in traits:
        if arg.lower() in line.lower():
            await ctx.send(line)
            #break
    opened.close()

@bot.command(name='insert')
async def insert(ctx, arg, arg1):
    opened = open("traits.txt", "r")
    traits = opened.readlines()
    opened.close()
    builder = '** ' + arg + ' ** - '+ arg1 + '\n'
    traits.append(builder)
    traits = sorted(traits)
    opened = open("traits.txt", "w")
    modified = "".join(traits)
    opened.write(modified)
    opened.close()

@bot.command(name='delete')
async def delete(ctx, arg):
    opened = open("traits.txt", "r")
    traits = opened.readlines()
    opened.close()
    modified = []
    for line in traits:
        if arg not in line:
            modified.append(line)
    modified = "".join(modified)
    opened = open("traits.txt", "w")
    opened.write(modified)
    opened.close()
    await ctx.send("Successfully deleted.")
