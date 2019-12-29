import discord
from discord.ext import commands
import datetime

client = commands.Bot(command_prefix = ':')
tokenFile = open('token.txt', 'r')
token = tokenFile.readline()

@client.event
async def on_ready():
    print(f'Online: Tetris99 Bot#7917 (ID: 651135979209621516)')

@client.event
async def on_member_join(member):
    memberMention = member.mention
    t99Server = client.get_guild(546595455983943690)
    modChannel = t99Server.get_channel(549452266864771102)
    dateNow, dateCreated = datetime.datetime.now(), member.created_at
    userSinceCreated = (dateNow - dateCreated).days * 24

    if userSinceCreated > 48:
        print(userSinceCreated)
    else:
        await t99Server.ban(user=member, reason="Account is less than 48 hours old")
        await modChannel.send(memberMention + '** has been kicked from the server for having an account under 48 hours old**')

client.run(token.strip())
