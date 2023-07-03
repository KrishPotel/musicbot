import discord
from discord.ext import commands

import sys, traceback
import os
from dotenv import load_dotenv

load_dotenv("Tokens.env")
BotToken = os.getenv('DISCORDTOKEN')

def get_prefix(bot, message):
    prefixes = ['!']

    if not message.guild:
        return '?'

    return commands.when_mentioned_or(*prefixes)(bot, message)

initial_extensions = ['cogs.owner','cogs.music']

bot = commands.Bot(command_prefix=get_prefix, description='yes', intents=discord.Intents().all())

@bot.event
async def on_ready():
    for extension in initial_extensions:
        await bot.load_extension(extension)

    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')

    # Changes our bots Playing Status. type=1(streaming) for a standard game you could remove type and url.
    await bot.change_presence(activity=discord.Game(name='doing stuff', type=1))
    print(f'Successfully logged in and booted...!')


bot.run(BotToken, reconnect=True)