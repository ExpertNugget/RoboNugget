import os
import discord
import sqlite3

# minor corrections for running dir, mainly for vsc
if "/src" in os.getcwd():
    pass
else:
    os.chdir('./src')


database = "./data/mpsdb.sqlite3"


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
with sqlite3.connect(database) as conn:
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS token (
        token TEXT PRIMARY KEY)
    """)

bot = discord.Bot()

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")


# grabs all files ending in .py in src/cogs, and stores them in a list minus the .py to load all cogs.
cog_list = [f[:-3] for f in os.listdir('./cogs') if f.endswith('.py')]

# Cogs disabled due to no longer or not working code
exclude_list = ['download', 'link', 'servers'] 

for cog in cog_list:
    # Skips cog if it's in the exclude list
    if cog in exclude_list:
        continue
    bot.load_extension(f'cogs.{cog}')


# keeps asking for a token until a valid token is provided
while True:
    try:
        with sqlite3.connect(database) as conn:
            cur = conn.cursor()
            cur.execute("SELECT token FROM token")
            TOKEN = cur.fetchone()  
        bot.run(TOKEN[0])
        break
    except Exception as e:  # Catch all exceptions
        print(f"An error occurred: {e}")
        TOKEN = input("Invalid token, enter Discord bot token:")
        with sqlite3.connect(database) as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO token (token) VALUES (?)", (TOKEN,))

