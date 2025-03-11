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

        if not urls:
            return

        modified_content = message.content

        def get_github_link_type(url):
            parsed = urlparse(url)
            if parsed.netloc != "github.com":
                return None

            path_parts = [p for p in parsed.path.split("/") if p]

            # GitHub Profile
            if len(path_parts) == 1:
                return f"GitHub Profile: {path_parts[0]}"

            # Repository root
            if len(path_parts) == 2:
                return f"GitHub Repo: {path_parts[0]}/{path_parts[1]}"

            # File or directory
            if len(path_parts) >= 3 and path_parts[2] in ["blob", "tree"]:
                branch = path_parts[3] if len(path_parts) > 3 else "main"
                item_type = "File" if path_parts[2] == "blob" else "Directory"
                return f"GitHub {item_type}: {path_parts[0]}/{path_parts[1]} ({branch})"

            # Issues
            if len(path_parts) >= 3 and path_parts[2] == "issues":
                if len(path_parts) >= 4 and path_parts[3].isdigit():
                    return f"GitHub Issue: #{path_parts[3]} in {path_parts[0]}/{path_parts[1]}"
                return f"GitHub Issues: {path_parts[0]}/{path_parts[1]}"

            # Pull Requests
            if len(path_parts) >= 3 and path_parts[2] == "pull":
                if len(path_parts) >= 4 and path_parts[3].isdigit():
                    return f"GitHub Pull Request: #{path_parts[3]} in {path_parts[0]}/{path_parts[1]}"
                return f"GitHub Pull Requests: {path_parts[0]}/{path_parts[1]}"

            # Default for other GitHub URLs
            return "GitHub Link"

        for url in set(urls):
            label = None
            parsed = urlparse(url)

            # Handle GitHub URLs
            if "github.com" in parsed.netloc:
                label = get_github_link_type(url)
            # Add other platforms here (e.g., GitLab, Bitbucket)

            # Default label for non-GitHub links
            if not label:
                domain = parsed.netloc.replace("www.", "")
                label = f"{domain.capitalize()} Link"

            hyperlink = f"[{label}]({url})"
            modified_content = modified_content.replace(url, hyperlink)

        webhooks = await message.channel.webhooks()
        for webhook in webhooks:
            if webhook.name == "Hyperlinker":
                webhook = webhook

        if webhook is None:
            webhook = await message.channel.create_webhook(name="Hyperlinker")
            print("Created webhook:", webhook.name)
            if webhook is None:
                print("Failed to create webhook")
                return

        try:
            async with aiohttp.ClientSession() as session:
                await webhook.send(
                    content=modified_content,
                    username=message.author.display_name,
                    avatar_url=message.author.display_avatar,
                )
        except Exception as e:
            print(e)
        else:
            await message.delete()


def setup(bot):
    bot.add_cog(hyperlinker(bot))
