import discord
from discord.ext import commands
import json
from mcuuid import MCUUID


class download(commands.Cog):  # create a class for our cog that inherits from commands.Cog
    # this class is used to create a cog, which is a module that can be added to the bot

    def __init__(self, bot):  # this is a special method that is called when the cog is loaded
        self.bot = bot

    download = discord.SlashCommandGroup("download")


def setup(bot):
    bot.add_cog(download(bot))
