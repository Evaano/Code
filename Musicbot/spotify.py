import discord
import re
import urllib.request
import asyncio
import pytube

client = discord.Client()
current_song = None

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Bad Life"))

@client.event
async def on_message(message):
    if message.content == '!join' or message.content == '!j':
        # Join the voice channel
        channel = message.author.voice.channel
        if channel is not None:
            voice = await channel.connect()
            print(f'Joined voice channel {channel}')
        else:
            await message.channel.send('You are not in a voice channel')

    elif message.content == '!disconnect' or message.content == '!dc':
        # Disconnect from the voice channel
        voice = discord.utils.get(client.voice_clients, guild=message.guild)
        if voice is not None:
            await voice.disconnect()
            print(f'Disconnected from voice channel')
        else:
            await message.channel.send('The bot is not connected to a voice channel')

    elif message.content.startswith('!play'):
        # Play a song
        if not message.author.voice:
            await message.channel.send('You are not in a voice channel')
            return

        voice = discord.utils.get(client.voice_clients, guild=message.guild)
        if voice is None:
            voice = await message.author.voice.channel.connect()

        song_name = message.content[6:].strip()
        await play_song(song_name, voice, message.channel)

    elif message.content == '!nowplaying':
        # Show the currently playing song
        if current_song is not None:
            await message.channel.send(f"Currently playing: {current_song}")
        else:
            await message.channel.send("No song is currently playing")
            
    elif message.content == '!stop':
        # Stop playing the current song
        voice = discord.utils.get(client.voice_clients, guild=message.guild)
        if voice is not None and voice.is_playing():
            voice.stop()
            current_song = None
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Bad Life"))
            await message.channel.send("Stopped playing the current song")
        else:
            await message.channel.send("No song is currently playing")

async def play_song(song_name, voice, channel):
    global current_song
    # Search for the song on YouTube
    query = song_name.replace(' ', '+')
    url = f'https://www.youtube.com/results?search_query={query}'
    html = urllib.request.urlopen(url)
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())

    if not video_ids:
        await channel.send(f"Sorry, I couldn't find the song {song_name} on YouTube.")
        return

    # Get the first search result
    video_url = f"https://www.youtube.com/watch?v={video_ids[0]}"
    video = pytube.YouTube(video_url)

    # Download the audio stream of the video
    audio_stream = video.streams.get_audio_only()
    audio_file = await asyncio.to_thread(audio_stream.download)

    # Play the song
    audio_source = await discord.FFmpegOpusAudio.from_probe(audio_file)
    if not voice.is_playing():
        voice.play(audio_source, after=lambda e: print('Player error: %s' % e) if e else None)
        await channel.send(f"Now playing: {video_url}")
        # Update bot's presence with the currently playing song
        global current_song
        current_song = song_name
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=song_name))

# Discord bot token
client.run('MTA3MzkwMTg1NzQ5NzQzMjA4NA.GO5IDh.yymMybaKoI1DH93QpNqS1nORzgyiOffjdvECU8')
