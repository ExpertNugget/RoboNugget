import discord
from discord.ext import commands
import sqlite3
import time
import re

database = "./data/mpsdb.sqlite3"

class logger(commands.Cog):  # create a class for our cog that inherits from commands.Cog
    # this class is used to create a cog, which is a module that can be added to the bot

    def __init__(self, bot):  # this is a special method that is called when the cog is loaded
        self.bot = bot

    logger = discord.SlashCommandGroup("logger")
    
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return
        # store the message content and author in variables
        content = message.content
        author = message.author
        with sqlite3.connect(database) as conn:
            cur = conn.cursor()
            cur.execute("SELECT * from users WHERE discord_id = ?", (author.id,))
            rows = cur.fetchall()
            column_names = [description[0] for description in cur.description]
            for row in rows:
                user_dict = dict(zip(column_names, row))
            try:
                log_thread_id = int(user_dict['log_thread_id'])
            except:
                log_thread_id = None
        with sqlite3.connect(database) as conn:
            cur = conn.cursor()
            cur.execute("INSERT OR REPLACE INTO configs (guild_id) VALUES (?)", (message.guild.id,))
            cur.execute("SELECT log_channel_id from configs WHERE guild_id = ?", (message.guild.id,))
            log_channel_id = int(re.sub("[^0-9]", "", str(cur.fetchone())))
            cur.execute("SELECT log_channel_id from configs WHERE guild_id = ?", (message.guild.id,))
            log_channel_webhook = str(cur.fetchone())
            
            cur.execute("SELECT log_channel_id from configs")
        if not log_channel_id:
            return
        print(log_channel_webhook)
        if log_thread_id: # log_thread_id found
            try: # check if thread still exists, else make new thread, otherwise update
                thread = self.bot.get_channel(log_thread_id) 
                await thread.send(content = content) # use the stored content variable
            except: # should only be here if original thread was deleted
                channel = self.bot.get_channel(log_channel_id)
                username = author.display_name # use the stored author variable
                current_time = str(int(time.time()))[:10]
                thread_message = f'Discord IDs:\n- `{author.id}` (logged by <@{self.bot.user.id}> <t:{current_time}:d>)' # use the stored author variable
                thread = await channel.create_thread(name = username, content = thread_message)
                with sqlite3.connect(database) as conn:
                    cur = conn.cursor()
                    cur.execute("INSERT OR REPLACE INTO users (log_thread_id, username, discord_id) VALUES (?, ?, ?)", (thread.id, author.display_name, author.id,))
                await thread.send(content = content) # use the stored content variable
        else: #log_thread_id not found, create thread
            channel = self.bot.get_channel(log_channel_id)
            username = author.display_name # use the stored author variable
            current_time = str(int(time.time()))[:10]
            thread_message = f'Discord IDs:\n- `{author.id}` (logged by <@{self.bot.user.id}> <t:{current_time}:d>)' # use the stored author variable
            thread = await channel.create_thread(name = username, content = thread_message)
            with sqlite3.connect(database) as conn:
                cur = conn.cursor()
                cur.execute("INSERT OR REPLACE INTO users (log_thread_id, username, discord_id) VALUES (?, ?, ?)", (thread.id, author.display_name, author.id,))
            await thread.send(content = content) # use the stored content variable

def setup(bot): 
    bot.add_cog(logger(bot))
