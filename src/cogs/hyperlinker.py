import discord
from discord.ext import commands
from urlextract import URLExtract
from urllib.parse import urlparse

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
            parsed_url = urlparse(url)
            github_pages = ['notifications', 'issues', 'new']
            if 'github.com' in parsed_url.netloc:
                path = parsed_url.path
                username = parsed_url.path.split("/")[1]
                if any(github_pages in username):
                    user_only = True
                    username = ''
                else:
                    username = parsed_url.path.split("/")[1]
                    
                if username:
                    repo = parsed_url.path.split("/")[2]
                if repo:
                    branch = parsed_url.path.split("/")[3]
                if branch: # checks if tree or blob
                    branch = parsed_url.path.split("/")[4] # replaces branch with actual branch name
                if branch:
                    file_path = parsed_url.path.split("/")[5]
                message.content.replace(url, hyperlink)
                
def setup(bot): 
    bot.add_cog(hyperlinker(bot))