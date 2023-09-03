import discord
from discord.ext import commands
import os
import toml


class update(commands.Cog):  # create a class for our cog that inherits from commands.Cog
    # this class is used to create a cog, which is a module that can be added to the bot

    def __init__(self, bot):  # this is a special method that is called when the cog is loaded
        self.bot = bot


def setup(bot):
    bot.add_cog(update(bot))
