import discord
from discord.ext import commands
from urlextract import URLExtract
from urllib.parse import urlparse
import aiohttp
from discord import Webhook


class hyperlinker(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        extractor = URLExtract()
        urls = extractor.find_urls(message.content)
        for url in urls:
            hyperlink = f"[{url}]({url})"
            parsed_url = urlparse(url)
            github_pages = ["notifications", "issues", "new"]
            username = parsed_url.path.split("/")[1]
            if "github.com" in parsed_url.netloc:
                if any(x in username for x in github_pages):
                    user_only = True
                else:
                    username = parsed_url.path.split("/")[1]
                if username:
                    repo = parsed_url.path.split("/")[2]
                if repo:
                    branch = parsed_url.path.split("/")[3]
                if branch:  # checks if tree or blob
                    branch = parsed_url.path.split("/")[
                        4
                    ]  # replaces branch with actual branch name
                if branch:
                    file_path = parsed_url.path.split("/")[5]
            message.content.replace(url, hyperlink)
        if urls:
            async with aiohttp.ClientSession() as session:
                webhook = Webhook.from_url(
                    "", session=session
                )  # todo: webhook management (make webhooks and reuse existing webhooks)
                await webhook.send(
                    content=message.content,
                    username=message.author.display_name,
                    avatar_url=message.author.display_avatar,
                )
        else:
            pass


def setup(bot):
    bot.add_cog(hyperlinker(bot))
