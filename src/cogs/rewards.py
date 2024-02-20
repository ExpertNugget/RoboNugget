import discord
from discord.ext import commands
from functions import fetchData
from config import databaseURL
from firebase_admin import db


class rewards(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return None
        ref = db.reference(
            path=f"/{message.guild.id}/{message.author.id}/userData/",
        )
        userData = fetchData(
            path=f"/{message.guild.id}/{message.author.id}/userData/",
            cache="rewardsCache",
        )
        if not userData:
            data = {
                "points": 0,
            }
            ref.set(data)
        points = int(userData["points"])
        points += 1
        data = {
            "points": str(points),
        }
        ref.set(data)


def setup(bot):
    bot.add_cog(rewards(bot))
