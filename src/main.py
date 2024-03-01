import os
import discord
from discord.ext import commands
from config import TOKEN
###> Dont remove they will be used -nugget
import firebase_admin
from firebase_admin import credentials, db
###! -nugget

###> firebase was being weird, will just use main db when ready -nugget
# cred = credentials.Certificate(firebaseKey)
# databaseApp = firebase_admin.initialize_app(cred, {"databaseURL": databaseURL})
###! -nugget

###> minor corrections for running dir, mainly for vsc -nugget
if "/src" in os.getcwd():
    pass
else:
    os.chdir("./src")
###! -nugget
    
bot = discord.Bot(intents=discord.Intents.all()) # having all intents just makes life easy, will change later -nugget

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")


# grabs all files ending in .py in src/cogs, and stores them in a list minus the .py to load all cogs. -nugget
cog_list = [f[:-3] for f in os.listdir("./cogs") if f.endswith(".py")]


@bot.slash_command(name="reload", description="[Owner Only] - Shutdown bot")
@commands.is_owner()
async def reload(ctx, cog: discord.Option(str, choices=cog_list)): # dunno why vsc is angy it works -nugget
    await ctx.defer()
    try:
        bot.reload_extension(f"cogs.{cog}")
        await ctx.respond(f"`{cog}.py` has been reloaded :)")
    except:
        await ctx.respond(f"`{cog}.py` has failed to reload :(")


###> These cogs are hard disabled due to pending work, to make them function -nugget
exclude_list = [
    "admin", # just unfinished, might make a cog just for configs -nugget
    "download", # Gotta get MC server up again to worry about this (also may want to modify so the seed and new chunks are incorrect) -nugget
    "hyperlinker", # semi functional, should look for api's to see if i can make it less jank and use the current as a backup if api fails -nugget
    "info", # need to migrate to new DB, and figure out organization (prob gonna move over to document db instead of json tree) -nugget
    "link", # surely with the new db this'll be easy, but need to get mc back to worry about it -nugget
    "rewards", # Looking to locally store a user points while they are active, then send to db when they A: go inactive for an hour or B: theres a query (from here or if i implement from streamerbot likely needs a api). -
    "servers", # Empty cog -nugget
    "stream", # Empty cog -nugget
    "util", # Empty cog -nugget
    "verification" # All sorts of broken, probably not gonna implement. -nugget
]
###! -nugget

for cog in cog_list:
    # Skips cog if it's in the exclude list -nugget
    if cog in exclude_list:
        continue
    try:
        bot.load_extension(f"cogs.{cog}")
    except:
        print(f"Failed to load {cog}")
        pass

bot.run(TOKEN)

### TODO first time setup for config.py -nugget
# Keeping for reference
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
### -nugget