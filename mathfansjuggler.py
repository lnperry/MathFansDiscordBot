import discord
import os
from datetime import datetime
from discord.ext import commands

client = commands.Bot(command_prefix='!')

user_queue = []

def get_channel(channel_str):
    for guild in client.guilds:
        for channel in guild.channels:
            if channel.name == channel_str:
                return channel


def get_guild(guild_str):
    for guild in client.guilds:
        if guild.name == guild_str:
            return guild

@client.event
async def on_ready():
    print('Bot is ready.')

@client.command()
async def done(ctx):
    guild_obj = get_guild('MathFanJuggler')
    print(f'queue length {len(user_queue)} and queue is {user_queue}')
    # if user queue empty
    if not user_queue:
        await ctx.send('No math fans in line!')
    else:
        user_popped = user_queue.pop(0)
        member = guild_obj.get_member(user_popped.id)
        # if user in text channel, reinstate permissions
        if ctx.author in get_channel('general').members:
            await guild_obj.get_member(member.id).edit(mute=False)
            await ctx.send(f'{member} unmuted')
        # if user in voice channel, unmute
        voice_channel = get_channel('General')
        if ctx.author in voice_channel.members:
            await voice_channel.set_permissions(ctx.author, speak=True)
            await ctx.send(f'{member} speak permissions set to true')
        await ctx.author.edit(mute=True)
        await ctx.send(
            f'{user_popped} is no longer in line and is now muted. There are {len(user_queue)} math fans in line.')


@client.command()
async def talk(ctx):
    # dynamically fetch guild object and member
    guild_obj = guild_obj = get_guild('MathFanJuggler')
    member = guild_obj.get_member(ctx.author.id)

    #if user already in line, do nothing
    if ctx.author in user_queue:
        await ctx.send(f'{ctx.author} already in line')
        return

    # if user queue empty
    if not user_queue:
        user_queue.append(ctx.author)
        # unmute member if in the voice channel, unmute
        if member in get_channel('General').members:
            await guild_obj.get_member(member.id).edit(mute=False)
            await ctx.send(f'{member} unmuted')

        # if user in text channel, reinstate permissions
        if member in get_channel('general').members:
            await guild_obj.get_member(member.id).edit(speak=True)
            await ctx.send(f'{member} speak permissions set to True')

        await ctx.send(f'No math fans in line. {ctx.author} unmuted.')
    else:
        user_queue.append(ctx.author)
        await ctx.send(f'{ctx.author} there are {len(user_queue) - 1} math fans ahead of you in line.')


@client.command()
async def bothelp(ctx):
    await ctx.send('!attendance {student name} logs the student to the attendance log\n'
                   '!talk adds the user to the voice queue\n'
                   '!done removes the user from the voice queue\n'
                   '!talkall unmutes all users in the server\n'
                   '!muteall mutes all users in the server\n')


@client.command()
async def talkall(ctx):
    # dynamically get guild ID
    guild_obj = get_guild('MathFanJuggler')
    print(f'channel {get_channel("General")}')
    # mute all members in the voice channel
    for member in get_channel('General').members:
        await guild_obj.get_member(member.id).edit(mute=False)

    # set all others speak=False
    voice_channel = get_channel('general')
    for member in voice_channel.members:
        await voice_channel.set_permissions(member, speak=True)

    await ctx.send('All users unmuted')


@client.command()
async def muteall(ctx):
    # dynamically get guild ID
    guild_obj = get_guild('MathFanJuggler')

    # mute all members in the voice channel
    for member in get_channel('General').members:
        await guild_obj.get_member(member.id).edit(mute=True)

    # set all others speak=False
    voice_channel = get_channel('general')
    for member in voice_channel.members:
        overwrite = discord.PermissionOverwrite()
        overwrite.speak = False
        await voice_channel.set_permissions(member, overwrite=overwrite)

    await ctx.send('All users muted')


@client.command()
async def attendance(ctx, *, student_name):
    time_now = datetime.now()
    attendance_path = os.path.join(os.getcwd(), 'attendance', f'attendance_{datetime.now().date()}.txt')
    attendance_file = open(attendance_path, 'a')
    attendance_file.write(f'{time_now.time()} {student_name}\n')
    attendance_file.close()
    await ctx.send(f'{student_name} is here')


client.run('Njg4MDgyMzI4NTI2MTI3MzU1.XmvIpg.z1pP98ga2N4deziM9SSH3dy4gZ8')

