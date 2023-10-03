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
        discord_id INTEGER NOT NULL,
        username TEXT,
        log_thread_id INTEGER
    );
    """)
with sqlite3.connect(database) as conn:
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS token (
        token TEXT PRIMARY KEY
    );
    """)
with sqlite3.connect(database) as conn:
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS bumpconfigs (
        guild_id INTEGER PRIMARY KEY NOT NULL,
        is_embed INTEGER DEFAULT "1" CHECK (is_embed IN (0,1)) NOT NULL,
        role_id INTEGER,
        ping_role INTEGER DEFAULT "0" CHECK (ping_role IN (0,1)) NOT NULL,
        thank_title TEXT DEFAULT "Thanks for bumping the server!",
        thank_description TEXT DEFAULT "I'll ping you when the next bump is ready. I'll remind again when the next bump is available {next-bump-count}" NOT NULL,
        remind_title TEXT DEFAULT "It's time to bump!",
        remind_description TEXT DEFAULT "Bump the server by running </bump:947088344167366698>" NOT NULL
    );
    """)
with sqlite3.connect(database) as conn:
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS configs (
        guild_id INTEGER PRIMARY KEY NOT NULL,
        staff_role_id INTEGER,
        log_channel_id INTEGER,
        log_channel_webhook TEXT
    );
    """)
with sqlite3.connect(database) as conn:
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS info (
        guild_id INTEGER PRIMARY KEY NOT NULL,
        staff_role_id INTEGER
    );
    """)


bot = discord.Bot(intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")


# grabs all files ending in .py in src/cogs, and stores them in a list minus the .py to load all cogs.
cog_list = [f[:-3] for f in os.listdir('./cogs') if f.endswith('.py')]

# These cogs are hard disabled due to pending work, to make them function
exclude_list = ['download', 'link', 'servers', 'admin'] 

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
            cur.execute("SELECT token FROM token;")
            TOKEN = cur.fetchone()  
        bot.run(TOKEN[0])
        break
    except Exception as e:  # Catch all exceptions
        print(f"An error occurred: {e}")
        TOKEN = input("Invalid token, enter Discord bot token:")
        with sqlite3.connect(database) as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO token (token) VALUES (?);", (TOKEN,))

