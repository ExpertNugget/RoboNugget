import discord
from discord.ext import commands
from config import databaseURL
from firebase_admin import db


class logger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    logger = discord.SlashCommandGroup("logger")

    ### TODO: convert to new DB
    # @commands.message_command(name="message source")
    # async def message_source(self, ctx, message: discord.Message):
    #    await ctx.defer
    #    with sqlite3.connect(database) as conn:
    #        cur = conn.cursor()
    #        cur.execute("SELECT * from configs WHERE guild_id = ?", (ctx.guild.id,))
    #        rows = cur.fetchall()
    #        column_names = [description[0] for description in cur.description]
    #        for row in rows:
    #            config_dict = dict(zip(column_names, row))
    #    log_channel_id = config_dict["log_channel_id"]
    #
    #    with sqlite3.connect(database) as conn:
    #        cur = conn.cursor()
    #        cur.execute(
    #            "SELECT * from logged_messages WHERE guild_id = ?", (ctx.guild.id,)
    #        )
    #        rows = cur.fetchall()
    #        column_names = [description[0] for description in cur.description]
    #        for row in rows:
    #            logged_messages_dict = dict(zip(column_names, row))
    #
    #    with sqlite3.connect(database) as conn:
    #        cur = conn.cursor()
    #        cur.execute("SELECT * from users WHERE guild_id = ?", (ctx.guild.id,))
    #        rows = cur.fetchall()
    #        column_names = [description[0] for description in cur.description]
    #        for row in rows:
    #            config_dict = dict(zip(column_names, row))
    #    channel = self.bot.get_channel(config_dict["log_channel_id"])

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return None
        if not message.content:
            return None
        GuildID = message.guild.id
        userID = message.author.id
        ref = db.reference(path=f"/GuildID/{GuildID}/loggerConfig", url=databaseURL)
        rawData = ref.get()
        isEnabled = rawData["isEnabled"]
        logChannelID = rawData["logChannelID"]
        if not isEnabled:
            return None
        ref = db.reference(
            path=f"/{GuildID}/{userID}/loggedMessages/{message.id}",
            url=databaseURL,
        )

        data = {
            "content": str(message.content),
            "channelID": str(message.channel.id),
            "createdAt": str(message.created_at),
        }
        ref.set(data)
        ### TODO: convert to new DB
        # with sqlite3.connect(database) as conn:
        #    cur = conn.cursor()
        #    cur.execute(
        #        "SELECT * from users WHERE discord_id = ?", (message.author.id,)
        #    )
        #    rows = cur.fetchall()
        #    column_names = [description[0] for description in cur.description]
        #    for row in rows:
        #        user_dict = dict(zip(column_names, row))
        #    try:
        #        log_thread_id = int(user_dict["log_thread_id"])
        #    except:
        #        log_thread_id = None
        # with sqlite3.connect(database) as conn:
        #    cur = conn.cursor()
        #    cur.execute("SELECT * from configs WHERE guild_id = ?", (message.guild.id,))
        #    rows = cur.fetchall()
        #    column_names = [description[0] for description in cur.description]
        #    for row in rows:
        #        config_dict = dict(zip(column_names, row))
        #    log_channel_id = config_dict["log_channel_id"]
        #    log_channel_webhook = config_dict["log_channel_webhook"]
        # if not logChannelID:
        #    return


#
# if logChannelID:  # log_thread_id found
#    try:  # check if thread still exists, else make new thread, otherwise update
#        thread = self.bot.get_channel(logChannelID)
#        async with aiohttp.ClientSession() as session:
#            webhook = Webhook.from_url(log_channel_webhook, session=session)
#            await webhook.send(
#                content=message.content,
#                username=message.author.display_name,
#                avatar_url=message.author.display_avatar,
#                thread=thread,
#            )
#    except:  # should only be here if original thread was deleted
#        print("in exception")
#        channel = self.bot.get_channel(logChannelID)
#        username = message.author.display_name
#        current_time = str(int(time.time()))[:10]
#        thread_message = f"Discord IDs:\n- `{message.author.id}` (logged by <@{self.bot.user.id}> <t:{current_time}:d>)"
#        thread = await channel.create_thread(
#            name=username, content=thread_message
#        )
#        with sqlite3.connect(database) as conn:
#            cur = conn.cursor()
#            cur.execute(
#                "INSERT OR REPLACE INTO users (guild_id, log_thread_id, username, discord_id) VALUES (?, ?, ?, ?)",
#                (
#                    message.guild.id,
#                    thread.id,
#                    message.author.display_name,
#                    message.author.id,
#                ),
#            )
#        async with aiohttp.ClientSession() as session:
#            webhook = Webhook.from_url(log_channel_webhook, session=session)
#            await webhook.send(
#                content=message.content,
#                username=message.author.display_name,
#                avatar_url=message.author.display_avatar,
#                thread=thread,
#                wait=True,
#            )
# else:  # log_thread_id not found, create thread
#    channel = self.bot.get_channel(logChannelID)
#    username = message.author.display_name
#    current_time = str(int(time.time()))[:10]
#    thread_message = f"Discord IDs:\n- `{message.author.id}` (logged by <@{self.bot.user.id}> <t:{current_time}:d>)"
#    thread = await channel.create_thread(name=username, content=thread_message)
#    with sqlite3.connect(database) as conn:
#        cur = conn.cursor()
#        cur.execute(
#            "INSERT OR REPLACE INTO users (guild_id, log_thread_id, username, discord_id) VALUES (?, ?, ?, ?)",
#            (
#                message.guild.id,
#                thread.id,
#                message.author.display_name,
#                message.author.id,
#            ),
#        )
#    async with aiohttp.ClientSession() as session:
#        webhook = Webhook.from_url(log_channel_webhook, session=session)
#        await webhook.send(
#            content=message.content,
#            username=message.author.display_name,
#            avatar_url=message.author.display_avatar,
#            thread=thread,
#            wait=True,
#        )


def setup(bot):
    bot.add_cog(logger(bot))
