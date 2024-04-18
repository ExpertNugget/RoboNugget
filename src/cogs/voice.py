import discord
from discord.ext import commands, pages
from discord.commands import SlashCommandGroup
from discord import CategoryChannel


class voice(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    voice = SlashCommandGroup("voice", "Commands for testing ext.pages")

    @voice.command(name="list")
    async def voice_list(self, ctx: discord.ApplicationContext):
        """Demonstrates passing a list of strings as pages."""


        
        
            
        paginator = pages.Paginator(
            for channel in channels:
                if isinstance(channel, CategoryChannel):
                    for channel in channel.channels:
                        if isinstance(channel, discord.VoiceChannel):
                            yield channel
            pages=[
                discord.Embed(title="VC title here 1"),
                discord.Embed(title="VC title here 2"),
            ],
            show_disabled=False,
        )

        await paginator.respond(ctx.interaction, ephemeral=False)


def setup(bot):
    bot.add_cog(voice(bot))
