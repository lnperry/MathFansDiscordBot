import discord
import os
from datetime import datetime
from discord.ext import commands

client = commands.Bot(command_prefix='!')


# Change Per Server Deployment
token = 'bot_token'
user_queue = []
lesson_mode = None
teacher = 307362705684299777
server_name = 'Test Server'

def get_channel(channel_str):
    for guild in client.guilds:
        for channel in guild.channels:
            if channel.name == channel_str:
                return channel


def get_guild(guild_str):
    for guild in client.guilds:
        if guild.name == guild_str:
            return guild

def change_lesson_mode(bool):
    global lesson_mode
    lesson_mode = bool

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(name='with Numbers', type=discord.ActivityType.playing))
    print('Bot is ready.')

#checks for new member join and mutes them.
@client.event
async def on_voice_state_update(member, before, after):	
    # dynamically get guild/channel ID
    guild_obj = get_guild(server_name)
    voice_channel = get_channel('general')
    # checks if in lesson mode
    if lesson_mode == True:
        if before.channel is None and after.channel is not None:
            if member.id != teacher:
                overwrite = discord.PermissionOverwrite()
                overwrite.speak = True
                await guild_obj.get_member(member.id).edit(mute=True)
                await voice_channel.set_permissions(member, overwrite=overwrite)

#sub routine for done/forcedone to prompt next user
@client.command()
async def nextquestion(ctx):
    guild_obj = get_guild(server_name)
    if not user_queue:
        await ctx.send('Queue Empty')
        return
    member = guild_obj.get_member(user_queue[0].id)
    #unmute user in voice channel
    if member in get_channel('General').members:
        await guild_obj.get_member(member.id).edit(mute=False)
        await ctx.send(f'{member} unmuted')
        # if user in text channel, reinstate permissions
        if member in get_channel('general').members:
            await guild_obj.get_member(member.id).edit(speak=True)
            await ctx.send(f'{member} speak permissions set to True')
        await ctx.send(f'{newmember} is now asking his/her question')
        return
    #if member is not found, pop and retry
    else:
        user_queue.pop(0)
        await ctx.send(f'Unable to find {member} in voice channel, skipping to next user')
        await nextquestion(ctx)
        return

#allows current user to end their question
@client.command()
async def done(ctx):
    if lesson_mode != True:
        await ctx.send('Class is not in session.')
        return
        
    guild_obj = get_guild(server_name)
    print(f'queue length {len(user_queue)} and queue is {user_queue}')
    # if user queue empty
    if not user_queue:
        await ctx.send('No math fans in line!')
    #if user who is currently talking wants to stop
    elif ctx.message.author == user_queue[0]:
        user_popped = user_queue.pop(0)
        member = guild_obj.get_member(user_popped.id)
        # if user in text channel, reinstate permissions
        if ctx.author in get_channel('general').members:
            await guild_obj.get_member(member.id).edit(mute=True)
            await ctx.send(f'{member} unmuted')
        # if user in voice channel, unmute
        voice_channel = get_channel('General')
        if ctx.author in voice_channel.members:
            await voice_channel.set_permissions(ctx.author, speak=True)
            await ctx.send(f'{member} speak permissions set to true')
        await ctx.author.edit(mute=True)
        await ctx.send(
            f'{user_popped} is no longer in line and is now muted. There are {len(user_queue)} math fans in line.')
        #tag next user into their question
        await nextquestion(ctx)
    #if user isnt currently the person talking
    else:
        await ctx.send('You are not currently talking')

#allows instructor to toggle next user
@client.command()
async def forcedone(ctx):
    guild_obj = get_guild(server_name)
    if ctx.message.author.id != teacher:
        await ctx.send('Missing Permissions. Please check !help')
        return 
    
    if not user_queue:
        await ctx.send('No math fans in line!')
    else:
        user_popped = user_queue.pop(0)
        member = guild_obj.get_member(user_popped.id)
        # if user in text channel, reinstate permissions
        if ctx.author in get_channel('general').members:
            await guild_obj.get_member(member.id).edit(mute=True)
            await ctx.send(f'{member} unmuted')
        # if user in voice channel, unmute
        voice_channel = get_channel('General')
        if ctx.author in voice_channel.members:
            await voice_channel.set_permissions(ctx.author, speak=True)
            await ctx.send(f'{member} speak permissions set to true')
        await ctx.author.edit(mute=True)
        await ctx.send(
            f'{user_popped} is no longer in line and is now muted. There are {len(user_queue)} math fans in line.')
        #tag next user into their question
        await nextquestion(ctx)

#shows queue
@client.command()
async def queue(ctx):
    if user_queue:
        for member in user_queue:
            queuelist = []
            queuelist.append(member.name)
        await ctx.send(f'Current Queue: {queuelist}')
    else:
        await ctx.send('Queue is empty!')

#queues user to ask a question
@client.command()
async def talk(ctx):
    if lesson_mode != True:
        await ctx.send('Class is not in session.')
        return
    # dynamically fetch guild object and member
    guild_obj = get_guild(server_name)
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

#ends class
@client.command()
async def end(ctx):
    if ctx.message.author.id != teacher:
        await ctx.send('Missing Permissions. Please check !help')
        return 
    # dynamically get guild ID
    guild_obj = get_guild(server_name)
    print(f'channel {get_channel("General")}') #whats this line for?
    
    #sets lesson mode
    change_lesson_mode(False)


    # unmute all members in the voice channel
    for member in get_channel('General').members:
        await guild_obj.get_member(member.id).edit(mute=False)

    # set all others speak=False
    voice_channel = get_channel('general')
    for member in voice_channel.members:
        await voice_channel.set_permissions(member, speak=True)

    await ctx.send('All users unmuted')

#starts class
@client.command()
async def start(ctx):
    if ctx.message.author.id != teacher:
        await ctx.send('Missing Permissions. Please check !help')
        return 
    # dynamically get guild/channel ID
    guild_obj = get_guild(server_name)
    voice_channel = get_channel('general')
    
    
    # sets lesson mode
    change_lesson_mode(True)

    
    # mute all members in the voice channel
    for member in get_channel('General').members:
        if member.id != teacher:
            await guild_obj.get_member(member.id).edit(mute=True)

    # set all others speak=False
    for member in voice_channel.members:
        if member.id != teacher:
            overwrite = discord.PermissionOverwrite()
            overwrite.speak = False
            await voice_channel.set_permissions(member, overwrite=overwrite)

    await ctx.send('Lesson Started! All users muted')

#command to count attendence
@client.command()
async def attendance(ctx, *, student_name):
    time_now = datetime.now()
    normpath = os.path.normpath(os.getcwd())
    data_folder = Path(normpath)
    attendance_path = data_folder / 'Attendance' / f'attendance_{datetime.now().date()}.txt'
    attendance_path = PureWindowsPath(attendance_path)
    attendance_file = open(attendance_path, 'a')
    attendance_file.write(f'{time_now.time()} {student_name}\n')
    attendance_file.close()
    await ctx.send(f'{student_name} is here')

#bothelp command with refrence for users
@client.command()
async def bothelp(ctx):
    embed = discord.Embed(
        title = 'Bot Commands',
        description = 'Essential Commands for Users',
        color = discord.Colour.blue()
    )
    embed.set_thumbnail(url='https://i.imgur.com/v8CwNn0.png')
    embed.add_field(name='!attendance {student name}', value='logs the student to the attendance log', inline=False)
    embed.add_field(name='!talk', value='adds the user to the voice queue', inline=False)
    embed.add_field(name='!done', value='removes the user from the voice queue', inline=False)
    embed.add_field(name='!queue', value='shows current queue to ask questions', inline=False)
    embed.add_field(name='!forcedone', value='forcefully removes the user from the voice queue [Instructor Only]', inline=False)
    embed.add_field(name='!start', value='unmutes all users in the server [Instructor Only]', inline=False)
    embed.add_field(name='!end', value='mutes all users in the server [Instructor Only]', inline=False)

    await ctx.send(embed=embed)

client.run(token)