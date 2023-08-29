import discord
import os
import json
from mcuuid import MCUUID
from mcuuid.tools import is_valid_mojang_uuid, is_valid_minecraft_username
import re
import sqlite3

conn = sqlite3.connect('./data/users.db')
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS users (
            discord_id INTEGER PRIMARY KEY,
            mc_uuid TEXT
            )""")
#c.execute("INSERT INTO users VALUES ('616258229122498581', 'de8c6c90-4f04-4f44-875c-cb89573de564')")
#c.execute("SELECT * FROM users WHERE discord_id='166311283744964608'")
#print(c.fetchall())
conn.commit()
conn.close()

bot = discord.Bot()
info = bot.create_group("info")

@bot.event
async def on_ready():
  print(f"{bot.user} is ready and online!")

@info.command(name="addminecraft", description="Add info to an user")
async def addmc(ctx, user: discord.Member, uuid: str):
    trimmed_uuid = uuid.replace("-", "")
    if is_valid_mojang_uuid(trimmed_uuid):
        conn = sqlite3.connect('data/users.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users (
        discord_id INTEGER PRIMARY KEY,
        mc_uuid TEXT
        )''')
        c.execute("INSERT INTO users (discord_id, mc_uuid) VALUES (?, ?)", 
                  (user.id, trimmed_uuid))
        conn.commit()
        conn.close()
        player = MCUUID(uuid=trimmed_uuid)
        await ctx.respond(f"Minecraft account \"{player.name}\" linked to user <@{user.id}>!")
    else:
        await ctx.respond("Invalid minecraft UUID.")
  
@info.command(name="lookup",
                   description="[WIP] Shows all logged data on a given user")
async def lookup(ctx, user: discord.Member):
  with open('./data/users.json') as access_json:
    raw_data = json.load(access_json) 
    try:
      user_data = raw_data['data'][f'{user.id}']
      if user_data['mc-uuid'] != None:
        uuid = user_data['mc-uuid']
        player = MCUUID(uuid=f'{uuid}')
        embed = discord.Embed(title=f'{user}\'s Profile',
                            description=f'Minecraft Username {player.name}')
      else:  
        embed = discord.Embed(title=f'{user}\'s Profile',
                            description="This user has no linked accounts")
      await ctx.respond(embed=embed)
    except: # this should make a new json object under data with the set to `user.id`
        embed = discord.Embed(description="user not logged, this will be fixed once I figure out how to append data to a json file, in the mean time only accounts <@166311283744964608> and <@616258229122498581> work with this command. - Nugget")
        await ctx.respond(embed=embed)
    
bot.run(os.environ['TOKEN'])

