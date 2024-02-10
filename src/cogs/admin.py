import discord
from discord.ext import commands
import sqlite3

database = "./data/mpsdb.sqlite3"


class admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    admin = discord.SlashCommandGroup("admin")

    @admin.command(name="set-staff-role")
    @commands.has_permissions(
        admin=True
    )  ### this isn't working for some reason, will figure out tmr -Nugget
    async def set_staff(self, ctx, role: discord.Option(discord.Role)):
        await ctx.defer()
        with sqlite3.connect(database) as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT OR REPLACE INTO config (guild_id, admin_role_id) VALUES (?, ?)",
                (
                    ctx.guild.id,
                    role.id,
                ),
            )
        await ctx.respond("Selected role: " + role.name)


def setup(bot):
    bot.add_cog(admin(bot))
