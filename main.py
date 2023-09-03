import os
import discord
import json
from mcuuid import MCUUID
from mcuuid.tools import is_valid_mojang_uuid, is_valid_minecraft_username
import toml
import ftplib


bot = discord.Bot()
info = bot.create_group("info")
link = bot.create_group("link")

# Config template
config = {
    'Config': {
        'VERSION': '3'
    },
    'Discord': {
        'TOKEN': ''
    },
    'Minecraft': {
        'authtype': 'ftp'
    },
    'FTP': {
        'host': '',
        'user': '',
        'pass': ''
    }
}
if not os.path.isfile('config.toml'):
    with open('config.toml', 'w') as f:
        toml.dump(config, f)
    print('Config file created, add discord bot token and start the bot.')
    exit()
elif os.path.isfile('config.toml'):
    with open('config.toml', 'r') as f:
        data = toml.load(f)
    version = data['Config']['VERSION']
    if version != '3':
        print(
            'Error: Config version is outdated, rename your `config.toml` file or move to another folder and resart the bot')
        exit()


@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")


@link.command(name='minecraft', description='Link your minecraft account to discord')
async def minecraft(ctx, code: discord.Option(int)):
    await ctx.defer()
    code = str(code)
    with open("config.toml", "r") as f:
        data = toml.load(f)
    host = data['FTP']['host']
    user = data['FTP']['user']
    password = data['FTP']['pass']

    ftp = ftplib.FTP(host, user, password)
    ftp.encoding = "utf-8"

    with open('./data/auth.json', "wb") as f:
        ftp.retrbinary("RETR ./auth/auth.json", f.write)
    with open('./data/auth.json', 'r') as f:
        raw_data = json.load(f)
    codes = raw_data['codes']
    if code in codes:
        uuid = codes[f'{code}']['uuid']
        trimmed_uuid = uuid.replace("-", "")
        with open('./data/users.json', 'r') as f:
            raw_data = json.load(f)
        data = raw_data[f'{ctx.author.id}']['mc_uuid']
        if raw_data[f'{ctx.author.id}']['mc_uuid'] == None:
            raw_data[f'{ctx.author.id}']['mc_uuid'] = trimmed_uuid
        else:
            print('')
        with open("./data/users.json", 'w') as f:
            json.dump(data, f, indent=2)
        player = MCUUID(uuid=trimmed_uuid)
        await ctx.respond(f"Minecraft account \"{player.name}\" linked to user {ctx.author.display_name}!")
    else:
        await ctx.respond("Invalid code.")


@info.command(
    name="lookup",
    description="[WIP] Shows all logged data on a given user")
async def lookup(ctx, user: discord.Option(discord.Member) = None):
    await ctx.defer()
    with open('./data/users.json', 'r') as f:
        raw_data = json.load(f)
    try:
        if user == None:
            user = ctx.author
        else:
            data = raw_data[user.id]
        if data['mc-uuid'] != None:
            uuid = data['mc-uuid']
            player = MCUUID(uuid=f'{uuid}')
            embed = discord.Embed(title=f'{user.display_name}\'s Profile',
                                  description=f'Minecraft Username {player.name}')
        else:
            embed = discord.Embed(title=f'{user.display_name}\'s Profile',
                                  description="This user has no linked accounts.")
        await ctx.respond(embed=embed)
    except:  # this should make a new json object under data with the set to `user.id`
        with open('./data/users.json', 'w') as f:
            json.dump(raw_data, f, indent=2)
        embed = discord.Embed(
            title=f'{user.display_name}\'s Profile',
            description="This user has no linked accounts.",
            thumbnail=user.display_avatar.url,
            colour=user.colour)
        await ctx.respond(embed=embed)


cogs_list = [
    'update'
]

for cog in cogs_list:
    bot.load_extension(f'cogs.{cog}')


with open("config.toml", "r") as f:
    data = toml.load(f)
TOKEN = data['Discord']['TOKEN']
try:
    bot.run(TOKEN)
except:
    print('Error: Invalid or no Discord token, check `config.toml`')
    exit()
