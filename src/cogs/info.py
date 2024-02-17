import discord
from discord.ext import commands
import sqlite3

database = "./data/mpsdb.sqlite3"


class info(commands.Cog):  # create a class for our cog that inherits from commands.Cog
    # this class is used to create a cog, which is a module that can be added to the bot

    def __init__(self, bot):
        self.bot = bot

    info = discord.SlashCommandGroup("info")

    @info.command(
        name="lookup", description="[WIP] Shows all logged data on a given user"
    )
    async def lookup(self, ctx, user: discord.Option(discord.Member) = None):
        await ctx.defer()
        if user != None:
            pass
        else:
            user = ctx.author

        with sqlite3.connect(database) as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE discord_id = ?", (user.id,))
            rows = cur.fetchall()

        # Get the column names
        column_names = [description[0] for description in cur.description]

        for row in rows:
            # Create a dictionary where the keys are column names and the values are row values
            raw_data = dict(zip(column_names, row))

        # Now you can access each value using its column name
        # ex: discord_id = raw_data['discord_id']

        try:
            discord_id = raw_data["discord_id"]
        except:
            with sqlite3.connect(database) as conn:
                cur = conn.cursor()
                cur.execute(
                    "INSERT OR REPLACE INTO users (discord_id) VALUES (?)", (user.id,)
                )

        else:
            pass
        """
        try:
            is_alt = raw_data[f'{user.id}']['is_alt']
        except:
            is_alt = False
        if is_alt == True:
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
        """
        embed = discord.Embed(
            title=f"{user.display_name}'s Profile", thumbnail=user.display_avatar.url
        )
        """
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
                            value=f'[{twitch_user}](https://twitch.tv/{twitch_user})')
        # Send a message when the button is clicked
        """
        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(info(bot))
