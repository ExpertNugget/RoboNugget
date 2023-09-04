import discord
from discord.ext import commands
import json
from mcuuid import MCUUID


class info(commands.Cog):  # create a class for our cog that inherits from commands.Cog
    # this class is used to create a cog, which is a module that can be added to the bot

    def __init__(self, bot):  # this is a special method that is called when the cog is loaded
        self.bot = bot

    info = discord.SlashCommandGroup("info")

    @info.command(
        name="lookup",
        description="[WIP] Shows all logged data on a given user")
    async def lookup(self, ctx, user: discord.Option(discord.Member) = None):
        await ctx.defer()
        with open('./data/users.json', 'r') as f:
            raw_data = json.load(f)
        try:
            if user == None:
                user = ctx.author
            else:
                data = raw_data[user.id]
            if data['mc-uuid'] != None:
                uuid = data['mc-uuid']
                player = MCUUID(uuid=f'{uuid}')
                embed = discord.Embed(title=f'{user.display_name}\'s Profile',
                                      description=f'Minecraft Username {player.name}')
            else:
                embed = discord.Embed(title=f'{user.display_name}\'s Profile',
                                      description="This user has no linked accounts.")
            await ctx.respond(embed=embed)
        except:  # this should make a new json object under data with the set to `user.id`
            with open('./data/users.json', 'w') as f:
                json.dump(raw_data, f, indent=2)
            embed = discord.Embed(
                title=f'{user.display_name}\'s Profile',
                description="This user has no linked accounts.",
                thumbnail=user.display_avatar.url,
                colour=user.colour)
            await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(info(bot))
