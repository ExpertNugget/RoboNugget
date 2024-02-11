import discord
from discord.ext import commands
import asyncio
import time
from config import databaseURL
from firebase_admin import db


class bump(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    bump = discord.SlashCommandGroup("bump-config")

    # Keeping for refrence
    # Disabled, i'll get it working tmr -Nugget
    # @bump.command(name="remind-title")
    # async def remind_title(self, ctx, title: discord.Option(str)):
    #    await ctx.defer()
    #    with sqlite3.connect(database) as conn:
    #        cur = conn.cursor()
    #        cur.execute("SELECT * from configs WHERE guild_id = ?", (ctx.guild.id,))
    #        rows = cur.fetchall()
    #        column_names = [description[0] for description in cur.description]
    #        for row in rows:
    #            raw_data = dict(zip(column_names, row))
    #        staff_id = raw_data[staff_role_id]
    #    for role in ctx.author.roles:
    #        print(role)
    #        if role.id == staff_id:
    #            with sqlite3.connect(database) as conn:
    #                cur = conn.cursor()
    #                cur.execute("INSERT OR REPLACE INTO bumpconfigs (guild_id, remind_title) VALUES (?, ?)", (ctx.guild.id, title,))
    #            await ctx.respond(f'Set remind title to "{title}"')
    #        else:
    #            pass
    # @bump.command(name="remind-description")
    # async def remind_description(self, ctx, description: discord.Option(str)):
    #    await ctx.defer()
    #    with sqlite3.connect(database) as conn:
    #        cur = conn.cursor()
    #        cur.execute("INSERT OR REPLACE INTO bumpconfigs (guild_id, remind_description) VALUES (?, ?)", (ctx.guild.id, description,))
    #    await ctx.respond(f'Set remind description to "{description}"')
    #
    # @bump.command(name="thank-title")
    # async def thank_title(self, ctx, title: discord.Option(str)):
    #    await ctx.defer()
    #    with sqlite3.connect(database) as conn:
    #        cur = conn.cursor()
    #        cur.execute("INSERT OR REPLACE INTO bumpconfigs (guild_id, thank_title) VALUES (?, ?)", (ctx.guild.id, title,))
    #    await ctx.respond(f'Set thank title to "{title}"')
    #
    # @bump.command(name="thank-description")
    # async def thank_description(self, ctx, description: discord.Option(str)):
    #    await ctx.defer()
    #    with sqlite3.connect(database) as conn:
    #        cur = conn.cursor()
    #        cur.execute("INSERT OR REPLACE INTO bumpconfigs (guild_id, thank_description) VALUES (?, ?)", (ctx.guild.id, description,))
    #    await ctx.respond(f'Set remind description to "{description}"')
    #
    # @bump.command(name="embed")
    # async def embed(self, ctx, embeds: discord.Option(str, choices=["enabled", "disabled"])):
    #    await ctx.defer()
    #    if embeds == "enabled":
    #        is_embed=1
    #    else:
    #        is_embed=0
    #    with sqlite3.connect(database) as conn:
    #        cur = conn.cursor()
    #        cur.execute("INSERT OR REPLACE INTO bumpconfigs (guild_id, is_embed) VALUES (?, ?)", (ctx.guild.id, is_embed,))
    #    await ctx.respond(f'Embeds are now {embeds}')
    #
    #
    # @bump.command(name="role")
    # async def role(self, ctx, description: discord.Option(str)):
    #    await ctx.defer()
    #    with sqlite3.connect(database) as conn:
    #        cur = conn.cursor()
    #        cur.execute("INSERT OR REPLACE INTO bumpconfigs (guild_id, remind_description) VALUES (?, ?)", (ctx.guild.id, description,))
    #    await ctx.respond(f'Set remind description to "{description}"')
    # Disabled, i'll get it working tmr -Nugget

    # todo
    # on_start
    # check last bump time, if under 2 hrs start timer with remaining time til 2 hrs from bump time
    # otherwise just send the reminder
    # todo

    @commands.Cog.listener()
    async def on_message(self, message):
        print("listener ran")
        channel = message.channel
        GuildID = message.guild.id
        if not message.author.id == 302050872383242240:
            return None
        for embed in message.embeds:
            if "Bump done!" in embed.description:
                ref = db.reference(
                    path=f"/GuildID/{GuildID}/bumpConfig", url=databaseURL
                )
                raw_data = ref.get()
                is_embed = raw_data["is_embed"]
                thank_title = raw_data["thank_title"]
                thank_description = str(raw_data["thank_description"])
                remind_description = raw_data["remind_description"]
                remind_title = raw_data["remind_title"]
                ping_role = raw_data["ping_role"]
                role_id = raw_data["role_id"]
                embed = ""
                content = ""
            if "{role}" in thank_description:
                thank_description = thank_description.replace(
                    "{role}", f"<@&{role_id}>"
                )
            if "{next-bump-count}" in thank_description:
                current_epoch_time = int(str(int(time.time()))[:10])
                epoch_time_plus_two_hours = current_epoch_time + 2 * 3600
                thank_description = thank_description.replace(
                    "{next-bump-count}", f"<t:{str(epoch_time_plus_two_hours)}:R>"
                )
            if is_embed:
                embed = discord.Embed(title=thank_title, description=thank_description)
            else:
                if thank_title:
                    content = thank_title + "\n" + thank_description
                else:
                    content = thank_description
            await channel.send(content=content, embed=embed)
            content = ""
            await asyncio.sleep(7200)  # waits 2 hours
            if ping_role:
                content = f"<@&{role_id}>"
            if is_embed:
                embed = discord.Embed(
                    title=remind_title, description=remind_description
                )
            else:
                if remind_title:
                    content = content + "\n" + remind_title + "\n" + remind_description
                else:
                    content = content + "\n" + remind_description
            await channel.send(content=content, embed=embed)


def setup(bot):
    bot.add_cog(bump(bot))
