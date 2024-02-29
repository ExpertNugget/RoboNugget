import os
import discord
from discord.ext import commands
from config import *
import firebase_admin
from firebase_admin import credentials, db

try:
    cred = credentials.Certificate(firebaseKey) 
    databaseApp = firebase_admin.initialize_app(cred, {"databaseURL": databaseURL})
except:
    print('no db')
# minor corrections for running dir, mainly for vsc
if "/src" in os.getcwd():
    pass
else:
    os.chdir("./src")

bot = discord.Bot(intents=discord.Intents.all())


@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")


# grabs all files ending in .py in src/cogs, and stores them in a list minus the .py to load all cogs.
cog_list = [f[:-3] for f in os.listdir("./cogs") if f.endswith(".py")]


@bot.slash_command(name="reload", description="[Owner Only] - Shutdown bot")
@commands.is_owner()
async def reload(ctx, cog: discord.Option(str, choices=cog_list)):  # type: ignore
    await ctx.defer()
    try:
        bot.reload_extension(f"cogs.{cog}")
        await ctx.respond(f"`{cog}.py` has been reloaded :)")
    except:
        await ctx.respond(f"`{cog}.py` has failed to reload :(")


# These cogs are hard disabled due to pending work, to make them function
exclude_list = [
    "admin",
    "download",
    "hyperlinker",
    "info",
    "link",
    "rewards",
    "servers",
    "stream",
    "util",
]
for cog in cog_list:
    # Skips cog if it's in the exclude list
    if cog in exclude_list:
        continue
    try:
        bot.load_extension(f"cogs.{cog}")
    except:
        print(f"Failed to load {cog}")
        pass

# moved to config.py
bot.run(TOKEN)
# TODO first time setup for config.py

# Keeping for refrence
# keeps asking for a token until a valid token is provided
# while True:
#    try:
#        with sqlite3.connect(database) as conn:
#            cur = conn.cursor()
#            cur.execute("SELECT token FROM token;")
#            TOKEN = cur.fetchone()
#        bot.run(TOKEN[0])
#        break
#    except Exception as e:  # Catch all exceptions
#        print(f"An error occurred: {e}")
#        TOKEN = input("Invalid token, enter Discord bot token:")
#        with sqlite3.connect(database) as conn:
#            cur = conn.cursor()
#            cur.execute("INSERT INTO token (token) VALUES (?);", (TOKEN,))
