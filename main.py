import os
import discord
import json
from mcuuid import MCUUID
from mcuuid.tools import is_valid_mojang_uuid, is_valid_minecraft_username
import toml

bot = discord.Bot()
info = bot.create_group("info")

# Config template
config = {
    'Config': {
        'VERSION': '2'
    },
    'Discord': {
        'TOKEN': ''
    },
    'Minecraft': {
        'authtype': ''
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
    if version != '2':
        print('Error: Config version is outdated, rename your `config.toml` file or move to another folder and resart the bot')
        exit()


@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")


@info.command(name="addminecraft", description="Add info to an user")
async def addmc(ctx, user: discord.Member, uuid: str):
    trimmed_uuid = uuid.replace("-", "")
    if is_valid_mojang_uuid(trimmed_uuid):
        with open('./data/users.json', 'r') as f:
            data = json.load(f)
        data['data'][f'{user.id}']['mc-uuid'] = f'{trimmed_uuid}'
        with open("./data/users.json", 'w') as f:
            json.dump(data, f, indent=2)
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
        except:  # this should make a new json object under data with the set to `user.id`
            embed = discord.Embed(
                description="user not logged, this will be fixed once I figure out how to append data to a json file, in the mean time only accounts <@166311283744964608> and <@616258229122498581> work with this command. - Nugget")
            await ctx.respond(embed=embed)

with open("config.toml", "r") as f:
    data = toml.load(f)
TOKEN = data['Discord']['TOKEN']
try:
    bot.run(TOKEN)
except:
    print('Error: Invalid or no Discord token')
    exit()
