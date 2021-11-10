import time
import os
from typing import List
import random
import discord
from discord import channel
from youtube_dl import YoutubeDL
from discord.utils import get
from discord import FFmpegPCMAudio
from discord.ext import commands



BRYAN = 196483088321085441
HOUSTON = 258323084145065984
OLIN = 199640591951331328


client = commands.Bot(command_prefix = '-')
balances = {}
player = []
queuePos = 0
bottoken = ''

with open('bottoken') as f:
    BOTTOKEN = f.read()

@client.event
async def on_ready():
    print('Bot is ready.')
    
@client.command()
async def ping(ctx):
    embedVar = discord.Embed(description=str(round(client.latency * 1000)) +'ms')
    await ctx.send(embed=embedVar)
    
@client.command()
async def HSpecial(ctx):
    message = ['\"Genshin at 10\"', '\"So as I was saying... \"', '\"I\'ll remember this\"', '\" Wait I forgot what I was saying\"', '\"Butter me up\"' 
                    , '\"That\'s not true...\"', '\"I never said that\"', '\"I\'m going to sleep\"', '\"Uhhhhh...\"\t\**Disconnects*\*' , '\"I want to be dominated\"' 
                    , '\"Let\'s Cheat guys" ']
    quote_Houston = '\n\t-Houston \'Bee\' Mak'
    #embedVar = discord.Embed(description=str(message[len(message) - 1] + quote_Houston))
    embedVar = discord.Embed(description=str(random.choice(message) + quote_Houston))
    await ctx.send(embed=embedVar)


@client.command()
async def smoothie(ctx):
    if (ctx.message.author.id == BRYAN or ctx.message.author.id == HOUSTON or ctx.message.author.id == OLIN):
        mess = ctx.message.content
        words = mess.split()
        if(words[3] in balances):
            if(words[2] == 'owes'):
                balances[words[3]] += int(words[4])
            elif(words[2] == 'paid'):
                balances[words[3]] -= int(words[4])
            else:
                await ctx.send(f'Invalid command, please use owes or paid')
        else:
            balances[words[3]] = int(words[4])

    else:
        await ctx.send(f'You are not authorized to handle Mango Bot')

@client.command()
async def balances(ctx):
    await ctx.send(balances)


@client.command()
async def play(ctx, url):
    
    voice_client = get(ctx.bot.voice_clients, guild=ctx.guild)
    connected =  voice_client and voice_client.is_connected()

    if (not connected):
        channel = ctx.message.author.voice.channel
        await channel.connect()

    
    ydl_opts = {'format': 'bestaudio', 'noplaylist':'False'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    voice = get(client.voice_clients, guild=ctx.guild)
    video = ''


    print('download before')
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        print('download after')
        
        if 'entries' in info:
            
            # Can be a playlist or a list of videos
            video = info['entries']

             #loops entries to grab each video_url
            for i, item in enumerate(video):
                song = {}
                URL = video[i]['webpage_url']     #url of video
                title = video[i]['title']           #title of video
                song['Video Title'] = title
                song['Video URL'] = URL
                
                player.append(song)

        else:
            video_title = info.get('title', None)
            song = {}
            song ['Video Title'] = video_title
            URL = info['formats'][0]['url']
            song['Video URL'] = URL

            player.append(song)
            print(player)


    if not voice.is_playing():
        voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS), after= lambda e: play_next(ctx))
        voice.is_playing()

def play_next(ctx):
    global queuePos
    queuePos += 1
    if len(player) <= queuePos:
        print('Reached end of queue')
    else:
        voice = get(client.voice_clients, guild=ctx.guild)
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        voice.play(FFmpegPCMAudio(player[queuePos]['Video URL'], **FFMPEG_OPTIONS), after= lambda e: play_next(ctx))



@client.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()
    global queuePos
    queuePos = 0
    global player
    player = []


client.run(BOTTOKEN)

