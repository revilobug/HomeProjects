"""
Program to enable conditional text mute
Has ability to poll for mutee to speak one message
Display mode to make everything pretty

author: Oliver Li
version: Winter2020
python: 3.8.5
"""

import discord
from discord.ext import commands
from datetime import datetime, timezone
import asyncio

#list of commands person could use
alex_speak = [
    '$reqauth',
    '$cage',
    '$uncage',
    '$blackoutMode',
    '$status'
]
#whether cage is on or off
speakmode = True
#who needs to be quiet
whoshuts = 0
#whether to display when he's talking
blackout = False

#change from UTC to Local time
def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)

#initiate client
client = commands.Bot(command_prefix = '$')

#when bot is online
@client.event
async def on_ready():
    print("Bot is ready.")

#whenever a message is received
#deletes messages if speaking is turned off
@client.event
async def on_message(message):
    global speakmode
    global blackout
    if (message.author == client.user):
        return

    #check if message was sent by who needs to stfu
    if (message.author.id == whoshuts):
        #if speakmode is false continue
        if (not speakmode):
            #if in blackout mode, just delete straight away
            if blackout:
                await message.delete()
                return

            #check if message is allowed
            if (message.content not in alex_speak):
                #make an embed of speaker info
                embed = discord.Embed(
                    title = message.author.display_name,
                    description = 'tried to speak!'
                )

                #set image embed of author
                embed.set_image(url = 'https://cdn.discordapp.com' + message.author.avatar_url._url)
                embed.set_footer(text = message.author.display_name + ' tried to talk on ' + str(utc_to_local(message.created_at)))

                #send the embed
                await message.channel.send(embed = embed)
                #delete the message
                await message.delete()
                # authorID = '<@' + str(message.author.id) + '>'
                # await message.channel.send('{} tried to speak on {}!'.format(message.author.mention, utc_to_local(message.created_at)))
                #await message.channel.send(f'https://tenor.com/view/alex-stfu-annoying-orange-gif-16941722')
    
    #disable commands if the message author is target and blackout mode is active
    if not (message.author.id == whoshuts and blackout):
        await client.process_commands(message)

@client.command()
async def spam(ctx, user: discord.User):
    authorID = '<@' + str(user.id) + '>'

    counter = 0
    while True:
        await ctx.send(format(authorID))
        counter += 1
        if  counter > 1000:
            break

#displays status of speakmode and blackout
@client.command()
async def status(ctx):
    global blackout
    global speakmode

    #stop if blackout mode is active
    if (ctx.author.id == whoshuts and blackout):
        return

    #make the author ID convertible
    authorID = '<@' + str(whoshuts) + '>'

    #if speaking is currently allowed
    if speakmode:
        await ctx.send(f'No one is currently caged!')
    else:
        await ctx.send('{} is currently caged'.format(authorID))
        await ctx.send('Blackout Mode is currently {}'.format(['OFF', 'ON'][blackout]))

#toggles blackoutMode
#blackout is more primitive and only deletes messages to prevent command spamming
@client.command()
@commands.has_role('Authority')
async def blackoutMode(ctx):
    global blackout

    #stop if blackout mode is active
    if (ctx.author.id == whoshuts and blackout):
        return
    
    #check if there is a target
    if (whoshuts == 0):
        await ctx.send(f'No one to blackout!')
        return

    #flip blackout
    blackout = not blackout

    #send blackout status
    await ctx.send('Blackout Mode is now {}'.format(['OFF', 'ON'][blackout]))

#actual function to mute target
@client.command()
@commands.has_role('Authority')
async def cage(ctx, user: discord.User):
    global speakmode
    global whoshuts
    global blackout

    #stop if blackout mode is active
    if (ctx.author.id == whoshuts and blackout):
        return

    #turn off speaking priveleges
    speakmode = False
    #set the person to stfu
    whoshuts = user.id


    authorID = '<@' + str(whoshuts) + '>'
    #if speakmode is false, then cage is on
    await ctx.send('Chastity Cage is now ON for {} !'.format(authorID))

#unmutes target
@client.command()
@commands.has_role('Authority')
async def uncage(ctx):
    global speakmode
    global whoshuts
    global blackout

    #stop if blackout mode is active
    if (ctx.author.id == whoshuts and blackout):
        return

    #check if anyone is target
    if (speakmode or whoshuts == 0):
        await ctx.send('No one to uncage!')
        return

    #check if there is a dictator usurping power
    if (ctx.author.id == whoshuts):
        await ctx.send('Your dictator powers have no say in this')
        return
    else:
        #tell information
        authorID = '<@' + str(whoshuts) + '>'
        await ctx.send('Chastity Cage is now OFF for {} !'.format(authorID))
        #turn off cage
        speakmode = True
        whoshuts = 0

#allows target to request to type one message
@client.command()
async def reqauth(ctx):
    global speakmode
    global blackout

    #stop if black out mode is active
    if (ctx.author.id == whoshuts and blackout):
        return

    #check if command user is already able to talk
    if speakmode or ctx.author.id != whoshuts:
        await ctx.send(f'You can already talk!')
        return

    #make embed
    embed = discord.Embed(
        title = 'Let him speak?'
    )

    embed.set_image(url = 'https://cdn.discordapp.com' + ctx.author.avatar_url._url)
    embed.set_footer(text = 'should we really let ^ this guy speak???')

    #send embed
    react_message = await ctx.send(embed = embed)

    #add voting reactions
    await react_message.add_reaction('👍')
    await react_message.add_reaction('👎')

    #get the cache of the actual message
    msg = await react_message.channel.fetch_message(react_message.id)  # Can be None if msg was deleted
    
    #make check function for wait_for
    def checkReaction(reaction, user):
        return reaction.count > 3 and str(reaction.emoji) == '👍'

    try:
        #wait until checkReaction is true or until timeout
        enableSpeech = await client.wait_for('reaction_add', 
                                                timeout=90.0, 
                                                check = checkReaction)

    #if timeout happens
    except asyncio.TimeoutError:
        await ctx.send(f'Not enough approvals, speech not allowed!')
        return

    #if wait_for condition is met
    if enableSpeech:
        #if there are more downvotes than upvotes, condition is not met
        if msg.reactions[1].count > msg.reactions[0].count:
            await ctx.send(f'Too many downvotes! sorry!')
            return
        else:
            #enable speech
            await ctx.send(f'speech enabled!')
            speakmode = True
            #wait for a message or for timeout
            try:
                await client.wait_for('message',
                                      timeout = 20.0)
            #if there is a timeout
            except asyncio.TimeoutError:
                await ctx.send("Time's up buddy, should've spoke while you could!")

            #disable speech again
            speakmode = False

#use token to run program
client.run('Nzk2MjMzNjExMzcyMDAzMzM4.X_U8Vg.a95KIgFJhX6NLlz18xaDmA2cbvA')