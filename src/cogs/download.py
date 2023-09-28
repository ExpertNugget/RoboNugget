import discord
from discord.ext import commands
import toml
import ftplib
import json
from datetime import datetime, timezone


class download(commands.Cog):  # create a class for our cog that inherits from commands.Cog
    # this class is used to create a cog, which is a module that can be added to the bot

    def __init__(self, bot):  # this is a special method that is called when the cog is loaded
        self.bot = bot

    download = discord.SlashCommandGroup("download")

    @download.command(name='backup', description='download latest backup from mps server')
    async def backup(self, ctx):
        await ctx.defer()
        with open("data/config.toml", "r") as f:
            data = toml.load(f)
        host = data['FTP']['host']
        user = data['FTP']['user']
        password = data['FTP']['pass']

        ftp = ftplib.FTP(host, user, password)
        ftp.encoding = "utf-8"

        with open('./data/backups.json', "wb") as f:
            ftp.retrbinary("RETR ./backups/backups.json", f.write)
        with open('./data/backups.json', 'r') as f:
            raw_data = json.load(f)
        data = raw_data['backups']
        createtimes = []
        for backups in data:
            createtimes.append(backups['createTime'])
        for backups in data:
            if backups['createTime'] == max(createtimes):
                createtime = max(createtimes)
                timestamp = createtime // 1000
                dt = datetime.fromtimestamp(timestamp)
                dt_utc = dt.astimezone(timezone.utc)
                filename = dt_utc.strftime('%Y-%-m-%-d_%-H-%-M-%-S')
                file = './backups/' + filename + '.zip'
                with open('./data/backup.zip', "wb") as f:
                    ftp.retrbinary(f"RETR {file}", f.write)
                with open("data/config.toml", "r") as f:
                    data = toml.load(f)
                api = MediaFireApi()
                session = api.user_get_session_token(
                    email=data['MediaFire']['email'],
                    password=data['MediaFire']['password'],
                    app_id=data['MediaFire']['app_id']
                )
                api.session = session
                uploader = MediaFireUploader(api)
                with open('./data/backup.zip', 'rb') as fd:
                    result = uploader.upload(fd, 'Some filename.txt',
                                             folder_key='1234567890123')
                embed = discord.Embed(
                    title=backups["worldName"],
                    description=f'Creation Date: <t:{timestamp}:f> (<t:{timestamp}:R>)'
                )

        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(download(bot))
