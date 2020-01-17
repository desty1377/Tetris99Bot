import discord
from discord.ext import commands
import datetime
import json
import asyncio
from libneko import pag

client = commands.Bot(command_prefix = ';')
tokenFile = open('token.txt', 'r')
token = tokenFile.readline()

@client.event
async def on_ready():
    print('Online: Tetris99 Bot#7917 (ID: 651135979209621516)')

@client.event
async def on_member_join(member):
    memberMention = member.mention
    t99Server = client.get_guild(546595455983943690)
    modChannel = t99Server.get_channel(549452266864771102)
    dateNow, dateCreated = datetime.datetime.now(), member.created_at
    userSinceCreated = (dateNow - dateCreated).days * 24

    if userSinceCreated > 48:
        #print(userSinceCreated)
        pass
    else:
        await t99Server.ban(user=member, reason="Account is less than 48 hours old")
        await modChannel.send(memberMention + '** has been kicked from the server for having an account under 48 hours old**')

@client.command(name = 'ping')
async def ping(ctx):
    await ctx.send(f'{ctx.author.mention} Pong!')

@pag.embed_generator(max_chars=2048, provides_numbering=True)
def leaderboard_embed(paginator, page, page_index):
    embed = discord.Embed(title = 'Tetris 99 Level Leaderboard', color=0xff0000)
    embed.set_thumbnail(url='https://bit.ly/37pTkCz')
    embed.add_field(name = f'Rankings page {page_index + 1}', value = page)
    embed.set_footer(text = 'Provide a picture in #role-request or #the-watch showing that you are level 20★ or higher and you will be added to this leaderboard!')
    return embed

@client.command(name = 'leaderboard')
async def leaderboard(ctx):
    with open('leaderboard.json', 'r') as f:
        leaderboardFile = json.load(f)
        sortedDict = {k: v for k, v in sorted(leaderboardFile.items(), key=lambda item: item[1], reverse=True)}
        
        nav = pag.EmbedNavigatorFactory(factory=leaderboard_embed, max_lines = 20)

        for player in sortedDict:
            if sortedDict[player] % 99 == 0:
                level = 99
                stars = (sortedDict[player] // 99 - 1) * '★'
            else:
                level = sortedDict[player] % 99
                stars = sortedDict[player] // 99 * '★'
            nav += f'{player} - {level} {stars} \n'
        
        nav.start(ctx)

@client.command(name = 'leaderboardadd', aliases = ['lbadd'])
async def leaderboardadd(ctx, playerName, playerLevelStr):
    t99Server = client.get_guild(546595455983943690)
    leaderboardRole = t99Server.get_role('Leaderboard Editor')
    if leaderboardRole in ctx.author.roles == False:
        await ctx.send(f'{ctx.author.mention} You do not have permission to use that command.')
    else:
        with open('leaderboard.json', 'r+') as f:
            leaderboardFile = json.load(f)
        playerLevelInt = -99
        playerUpdate = False

        for character in playerLevelStr:
            if character == '*':
                playerLevelInt += 99

        if playerLevelStr[-2:] == '**':
            playerLevelInt += int(playerLevelStr[:len(playerLevelStr) - 2])
        else:
            playerLevelInt += int(playerLevelStr[:len(playerLevelStr) - 1])

        if playerName in leaderboardFile == True:
            playerUpdate = True

        leaderboardFile[playerName] = playerLevelInt
        with open('leaderboard.json', 'w') as f:
            json.dump(leaderboardFile, f)

        if playerUpdate == False:
            if playerLevelInt > 99:
                await ctx.send(f'{playerName} has been successfully added to the leaderboard with level {playerLevelInt - 99}★★')
            else:
                await ctx.send(f'{playerName} has been successfully added to the leaderboard with level {playerLevelInt}★')
        else:
            if playerLevelInt > 99:
                await ctx.send(f"{playerName}'s level has been updated to {playerLevelInt - 99}★★")
            else:
                await ctx.send(f"{playerName}'s level has been updated to {playerLevelInt}★")


@client.command(name='leaderboardremove', aliases=['lbremove'])
async def leaderboardremove(ctx, playerName):
    t99Server = client.get_guild(546595455983943690)
    leaderboardRole = t99Server.get_role('Leaderboard Editor')
    if leaderboardRole in ctx.author.roles == False:
        await ctx.send(f'{ctx.author.mention} You do not have permission to use that command.')
    else:
        with open('leaderboard.json', 'r+') as f:
            leaderboardFile = json.load(f)

        try:
            del leaderboardFile[playerName]
        except KeyError:
            await ctx.send(f'{ctx.author.mention} No player could be found with that name.')
        else:
            await ctx.send(f'{ctx.author.mention} {playerName} has been removed from the leaderboard.')


@client.command(name='countdown', aliases=['cd', 'count'])
async def countdown(ctx, time):
    try:
        time = int(time)
    except ValueError:
        await ctx.send(f'{ctx.author.mention} Please input a valid amount of time to count down from.')
    else:
        if time <= 2:
            await ctx.send(f'{ctx.author.mention} Please input a number that is 3 or larger to count down from.')
        else:
            leaderboardEmbed = discord.Embed(title = 'Countdown', color=0xff0000)
            leaderboardEmbed.set_thumbnail(url='https://bit.ly/37pTkCz')
            leaderboardEmbed.add_field(name = f'Counting down from {time}!', value = 'Countdown begins in 5 seconds! Be ready!')
            leaderboardMessage = await ctx.send(embed=leaderboardEmbed)
            await asyncio.sleep(5)

            for i in range(1, time):
                leaderboardEmbed = discord.Embed(title = 'Countdown', color=0xff0000)
                leaderboardEmbed.set_thumbnail(url='https://bit.ly/37pTkCz')
                leaderboardEmbed.add_field(name = f'Counting down from {time}!', value = f'`{time}!`')
                await leaderboardMessage.edit(embed=leaderboardEmbed)
                await asyncio.sleep(1)

            leaderboardEmbed = discord.Embed(title = 'Countdown completed!', color=0xff0000)
            leaderboardEmbed.set_thumbnail(url='https://bit.ly/37pTkCz')
            leaderboardEmbed.add_field(name = f'Counting down from {time}!', value = '`Go!` Good luck!')

@client.command(name='countdownrole',  aliases=['cdrole'])
async def countdownrole(ctx):
    t99Server = client.get_guild(546595455983943690)
    countdownRole = discord.utils.get(ctx.guild.roles, name='Countdown')
    user = ctx.message.author
    if countdownRole in ctx.author.roles:
        await user.remove_roles(countdownRole)
        await ctx.send(f'The countdown command has been removed from {ctx.author}')
    else:
        await user.add_roles(countdownRole)
        await ctx.send(f'The countdown command has been given to {ctx.author}')

@client.command(name='pingrole', aliases=['prole'])
async def pingrole(ctx):
    t99Server = client.get_guild(546595455983943690)
    pingRole = discord.utils.get(ctx.guild.roles, name='Ping')
    user = ctx.message.author
    if pingRole in ctx.author.roles:
        await user.remove_roles(pingRole)
        await ctx.send(f'The ping command has been removed from {ctx.author}')
    else:
        await user.add_roles(pingRole)
        await ctx.send(f'The ping command has been given to {ctx.author}')

client.run(token.strip())
