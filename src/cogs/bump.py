import discord
from discord.ext import commands
import asyncio

class bump(commands.Cog): 

    def __init__(self, bot): 
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message, channel):
        if message.author == 302050872383242240:
            for embed in message.embeds:
                if "Bump done!" in embed.description:
                    await asyncio.sleep(7200)
                    content = '<@836263721281650718>'
                    embed = discord.Embed(
                        title='It\'s time to bump!',
                        description='Bump the server by running </bump:947088344167366698>'
                    )

                    await channel.send(content = content, embed = embed)

        
def setup(bot):
    bot.add_cog(bump(bot))