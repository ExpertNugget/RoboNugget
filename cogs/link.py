import discord
from discord.ext import commands
import toml
import ftplib
from mcuuid import MCUUID
import json


class link(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    link = discord.SlashCommandGroup("link")

    @link.command(name='minecraft', description='Link your minecraft account to discord')
    async def minecraft(self, ctx, code: discord.Option(int)):
        await ctx.defer()
        code = str(code)
        with open("config.toml", "r") as f:
            data = toml.load(f)
        host = data['FTP']['host']
        user = data['FTP']['user']
        password = data['FTP']['pass']

        ftp = ftplib.FTP(host, user, password)
        ftp.encoding = "utf-8"

        with open('./data/auth.json', "wb") as f:
            ftp.retrbinary("RETR ./auth/auth.json", f.write)
        with open('./data/auth.json', 'r') as f:
            raw_data = json.load(f)
        codes = raw_data['codes']
        if code in codes:
            uuid = codes[f'{code}']['uuid']
            trimmed_uuid = uuid.replace("-", "")
            with open('./data/users.json', 'r') as f:
                raw_data = json.load(f)
            data = raw_data[f'{ctx.author.id}']['mc_uuid']
            if raw_data[f'{ctx.author.id}']['mc_uuid'] == None:
                raw_data[f'{ctx.author.id}']['mc_uuid'] = trimmed_uuid
            else:
                print('')
            with open("./data/users.json", 'w') as f:
                json.dump(data, f, indent=2)
            player = MCUUID(uuid=trimmed_uuid)
            await ctx.respond(f"Minecraft account \"{player.name}\" linked to user {ctx.author.display_name}!")
        else:
            await ctx.respond("Invalid code.")


def setup(bot):
    bot.add_cog(link(bot))
