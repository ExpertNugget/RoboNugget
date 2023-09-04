import discord
from discord.ext import commands
import toml
import ftplib
import json


class download(commands.Cog):  # create a class for our cog that inherits from commands.Cog
    # this class is used to create a cog, which is a module that can be added to the bot

    def __init__(self, bot):  # this is a special method that is called when the cog is loaded
        self.bot = bot

    download = discord.SlashCommandGroup("download")

    @download.command(name='backup', description='download latest backup from mps server')
    async def backup(self, ctx):
        await ctx.defer()
        with open("config.toml", "r") as f:
            data = toml.load(f)
        host = data['FTP']['host']
        user = data['FTP']['user']
        password = data['FTP']['pass']

        ftp = ftplib.FTP(host, user, password)
        ftp.encoding = "utf-8"

        with open('./data/backups.json', "wb") as f:
            ftp.retrbinary("RETR ./backups/backups.json", f.write)
        with open('./data/backups.json', 'r') as f:
            raw_data = json.load(f)
        data = raw_data['backups']
        print(data)
        await ctx.respond('potatoes')


def setup(bot):
    bot.add_cog(download(bot))
