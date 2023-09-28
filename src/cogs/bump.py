#!/usr/bin/env python3
import discord
from discord.ext import commands
import asyncio

class bump(commands.Cog): 

    def __init__(self, bot): 
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        #ignores non bots
        if not message.author.bot:
            return
        channel = message.channel
        if message.author.id == 302050872383242240:
            print('author confirm to be disboard\nchecking embed')
            print(message.embeds)
            for embed in message.embeds:
                print(embed)
                if "Bump done!" in embed.description:
                    print('embed matched')
                    embed = discord.Embed(
                        title="Thank you for bumping the server!",
                        description="I'll ping <@836263721281650718> when the server can be bumped again."
                    )
                    
                    await channel.send(embed=embed)
                    # waits 2 hours and sends a followup
                    print('waiting 2 hours for next response')
                    await asyncio.sleep(7200)
                    content = '<@836263721281650718>'
                    embed = discord.Embed(
                        title='It\'s time to bump!',
                        description='Bump the server by running </bump:947088344167366698>'
                    )
                    await channel.send(content=content, embed=embed)
                else:
                    return
        else:   
            return

class MyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        # Ignore messages from non-bots
        if not message.author.bot:
            return

        # Do something with the bot message
        print(message.content)

def setup(bot): 
    bot.add_cog(bump(bot))