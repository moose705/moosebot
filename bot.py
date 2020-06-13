import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='%')

# needed to split commands between modules
# whiiich i dont do since most commands use globals defined in main 
# but if i ever did want to
# having this in its own file would be useful.