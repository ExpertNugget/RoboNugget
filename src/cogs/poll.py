import discord
from discord.ext import commands


class poll(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Create ranked poll context menu command for message with poll
    #@discord.user_command(name="Ranked Poll")
    #async def ranked_poll(ctx, message: discord.Message):
    #    poll = message.poll
    #    if poll is None:
    #        await ctx.respond("This is not a poll")
    #        return
        
def setup(bot):
    bot.add_cog(poll(bot))
