import discord
from discord.ext import commands
import ftplib
from mcuuid import MCUUID


class link(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    link = discord.SlashCommandGroup("link")

    @link.command(
        name="minecraft", description="Link your Minecraft account to Discord"
    )
    async def minecraft(self, ctx, code: discord.Option(int)):
        await ctx.defer()
        code = str(code)
        with open("src/data/config.toml", "r") as f:
            data = toml.load(f)
        host = data["FTP"]["host"]
        user = data["FTP"]["user"]
        password = data["FTP"]["pass"]

        ftp = ftplib.FTP(host, user, password)
        ftp.encoding = "utf-8"

        with open("src/data/auth.json", "wb") as f:
            ftp.retrbinary("RETR ./auth/auth.json", f.write)
        with open("src/data/auth.json", "r") as f:
            raw_data = json.load(f)
        codes = raw_data["codes"]
        if code in codes:
            uuid = codes[f"{code}"]["uuid"]
            trimmed_uuid = uuid.replace("-", "")
            with open("src/data/users.json", "r") as f:
                raw_data = json.load(f)
            data = raw_data[f"{ctx.author.id}"]["mc_uuid"]
            if raw_data[f"{ctx.author.id}"]["mc_uuid"] == None:
                raw_data[f"{ctx.author.id}"]["mc_uuid"] = trimmed_uuid
            else:
                print("")
            with open("src/data/users.json", "w") as f:
                json.dump(data, f, indent=2)
            player = MCUUID(uuid=trimmed_uuid)
            await ctx.respond(
                f'Minecraft account "{player.name}" linked to user {ctx.author.display_name}!'
            )
        else:
            await ctx.respond("Invalid code.")

    @link.command(name="twitch", description="Link your Twitch account to Discord")
    async def twitch(self, ctx, code: discord.Option(int)):
        await ctx.defer()
        code = str(code)
        await ctx.respond("Not made yet :p - Nugget")


def setup(bot):
    bot.add_cog(link(bot))
