import os
import discord
import toml
import sqlite3

database = "src/data/mpsdb.sqlite3"


with sqlite3.connect(database) as conn:
    cur = conn.cursor()
    # temp solution for data storage until main database is working
    cur.execute("""
    
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        discord_id INTEGER NOT NULL
    )
    """)
with sqlite3.connect(database) as conn:
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS configs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        guild_id INTEGER NOT NULL
    )
    """)

bot = discord.Bot()

# Config template
config = {'TOKEN': ''}
if not os.path.isfile('src/data/config.toml'):
    with open('src/data/config.toml', 'w') as f:
        toml.dump(config, f)
else:
    pass


@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")


# grabs all files ending in .py in src/cogs, and stores them in a list minus the .py to load all cogs.
cog_list = [f[:-3] for f in os.listdir('src/cogs') if f.endswith('.py')]

# Cogs disabled due to no longer or not working code
exclude_list = ['download', 'link', 'servers'] 

for cog in cog_list:
    # Skips cog if it's in the exclude list
    if cog in exclude_list:
        continue
    bot.load_extension(f'cogs.{cog}')


# keeps asking for a token until a valid token is provided
def startbot():
    with open("src/data/config.toml", "r") as f:
        data = toml.load(f)
    TOKEN = data['TOKEN']
    if TOKEN == None:
        TOKEN = data.get('TOKEN', input("Enter Discord bot token:"))
    else:
        pass
    while True:
        try:
            bot.run(TOKEN)
            data = {'TOKEN': TOKEN}
            with open("src/data/config.toml", "w") as f:
                toml.dump(data, f)
            break
        except:
            TOKEN = input("Invalid token, enter Discord bot token:")
startbot()