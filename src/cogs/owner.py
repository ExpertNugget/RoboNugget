import discord
from discord.ext import commands

class owner(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(description='[Owner Only] - Shutdown bot')
    @commands.is_owner()
    async def shutdown(self, ctx):
        await ctx.respond("Shutting down the bot...")
        await ctx.bot.logout()


def setup(bot):
    bot.add_cog(owner(bot))