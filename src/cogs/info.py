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
        if user != None:
            pass
        else:
            user = ctx.author
        if raw_data[f'{user.id}'] != None:
            pass
        else:
            raw_data[f'{user.id}'] = {}
            with open('./data/users.json', 'w') as f:
                json.dump(raw_data, f, indent=2)
        try:
            print('Is running')
            is_alt = raw_data[f'{user.id}']['is_alt']
            print(is_alt)
        except:
            is_alt = False
        print('before')
        if is_alt == True:
            print('im running')
            alt = user.id
            user_id = raw_data[f'{user.id}']['main_id']
            user = self.get_user(user_id)
        else:
            pass
        try:
            mcuuid = raw_data[f'{user.id}']['mc_uuid']
            try:
                mcuuid_alts = raw_data[f'{user.id}']['mc_uuid-alts']
            except:
                mcuuid_alts = None
        except:
            mcuuid = None
        try:
            twitch_user = raw_data[f'{user.id}']['twitch_user']
        except:
            twitch_user = None
        try:
            description = raw_data[f'{user.id}']['description']
        except:
            description = None
        try:
            colour = raw_data[f'{user.id}']['colour']
        except:
            colour = None

        embed = discord.Embed(
            title=f'{user.display_name}\'s Profile',
            description=description,
            thumbnail=user.display_avatar.url,
            colour=colour)

        if mcuuid != None:
            player = MCUUID(uuid=f'{mcuuid}')
            embed.add_field(name='Minecraft Username:', value=f'{player.name}')
            if mcuuid_alts != None:
                pass  # to be added
            else:
                pass
        else:
            pass
        if twitch_user != None:
            embed.add_field(name='Twitch Username:',
                            value=f'{twitch_user}')
        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(info(bot))
