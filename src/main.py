import discord, os, argparse
from discord.ext import commands

parser = argparse.ArgumentParser()
parser.add_argument("-dev", action="store_true")
args = parser.parse_args()

###> minor corrections for running dir, mainly for vsc -nugget
if "/src" in os.getcwd():
    pass
else:
    os.chdir("./src")
###! -nugget

if args.dev:
    with open("data/token-dev.txt", "r") as f:
        token = f.read()
else:
    with open("data/token.txt", "r") as f:
        token = f.read()


###> having all intents just makes life easy, will change later -nugget
bot = discord.Bot(intents=discord.Intents.all())
###! -nugget


@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")


###> grabs all files ending in .py in src/cogs, and stores them in a list minus the .py to load all cogs. -nugget
cog_list = [f[:-3] for f in os.listdir("./cogs") if f.endswith(".py")]
###! -nugget


@bot.slash_command(name="reload", description="[Owner Only] - Reloads a cog")
@commands.is_owner()
async def reload(ctx, cog=discord.Option(str, choices=cog_list)):
    await ctx.defer()
    try:
        bot.reload_extension(f"cogs.{cog}")
        await ctx.respond(f"`{cog}.py` has been reloaded :)")
    except:
        await ctx.respond(f"`{cog}.py` has failed to reload :(")


###> These cogs are hard disabled due to pending work, to make them function -nugget
exclude_list = [
    "logger",  # DB removed, needs rework
    "admin",  # just unfinished, might make a cog just for configs -nugget
    "download",  # Gotta get MC server up again to worry about this (also may want to modify the seed so people cant cheat) -nugget
    # "hyperlinker",  # semi functional, should look for api's to see if i can make it less jank and use the current as a backup if api fails -nugget
    "info",  # need to migrate to new DB, and figure out organization (prob gonna move over to document db instead of json tree) -nugget
    "link",  # surely with the new db this'll be easy, but need to get mc back to worry about it -nugget
    "rewards",  # Looking to locally store a user points while they are active, then send to db when they A: go inactive for an hour or B: theres a query (from here or if i implement from streamerbot likely needs a api). -
    "servers",  # Empty cog -nugget
    "settings",  # merging dev to main then trying to implement -nugget
    "stream",  # Empty cog -nugget
    "util",  # Empty cog -nugget
    "verification",  # All sorts of broken, probably not gonna implement. -nugget
    "voice",  # broked -nugget
]
###! -nugget

for cog in cog_list:
    ###> Skips cog if it's in the exclude list -nugget
    if cog in exclude_list:
        continue  # moves onto next cog
    ###! -nugget
    bot.load_extension(f"cogs.{cog}")  # loads cog -nugget
    ###> Attempts to load cogs and doesn't load if it fails -nugget
    # try:
    #    bot.load_extension(f"cogs.{cog}")  # loads cogs -nugget
    # except:
    #    print(f"Failed to load {cog}")
    #    pass  # moves onto next cog -nugget

bot.run(token)  # runs bot
