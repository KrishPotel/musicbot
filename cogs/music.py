from discord.ext import commands
from discord import VoiceClient
from youtube_dl import YoutubeDL
from discord import VoiceChannel
import discord
from requests import get
import requests
from discord import FFmpegPCMAudio
from discord.ext import commands
from discord.utils import get
import asyncio
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import youtubesearchpython
import os
from dotenv import load_dotenv

class MusicCog(commands.Cog):

    def __init__(self, bot):
        load_dotenv()
        self.bot = bot
        self.musicQ = []
        self.client_id = os.getenv("SpotifyClientId")
        self.client_secret = os.getenv("SpotifyClientSecret")
        client_credentials_manager = SpotifyClientCredentials(client_id=self.client_id, client_secret=self.client_secret)
        self.sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


    def search(self, query):
        with YoutubeDL({'format': 'bestaudio', 'noplaylist':'True'}) as ydl:
            try: requests.get(query)
            except: info = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
            else: info = ydl.extract_info(query, download=False)
        return (info, info['formats'][0]['url'])

    # Hidden means it won't show up on the default help.
    @commands.command(name='join', hidden=False)
    async def join(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        channel = ctx.author.voice.channel

        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
        
    async def playsong(self, ctx, song):
        #Solves a problem I'll explain later
        FFMPEG_OPTS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        source = song
        vc = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)

    # Check if the bot is already connected to a voice channel
        if vc and vc.is_connected():
            await vc.move_to(ctx.author.voice.channel)  # Move to the user's voice channel
        else:
            # Connect to the user's voice channel if not already connected
            channel = ctx.author.voice.channel
            vc = await channel.connect()

        vc.play(FFmpegPCMAudio(source, **FFMPEG_OPTS), after=lambda e: print('done', e))
    

    async def getSpotifySongs(self, playlist_url):
        results = self.sp.playlist_tracks(playlist_url)

        # Iterate over the playlist tracks
        for item in results['items']:
            track = item['track']
            track_name = track['name']
            artists = [artist['name'] for artist in track['artists']]
            print(f"Track: {track_name}")
            print(f"Artists: {', '.join(artists)}")
            print('---')

    @commands.command(name='play', hidden=False)
    async def play(self, ctx, *, query):

        if("open.spotify.com" in query):
           await self.getSpotifySongs(query)
        else:
            v,q = self.search(query)

            if(self.musicQ.__len__() <= 0):
                self.musicQ.append(q)
                await self.playsong(ctx, song=self.musicQ[0])
            else:
                self.musicQ.append(q)
                print(v["title"])

        while ctx.voice_client.is_playing():
            await asyncio.sleep(1)

        if(ctx.voice_client.is_playing()):
            print(ctx.voice_client.is_playing())
        else:
            self.musicQ.pop(0)
            if(self.musicQ.__len__() >= 0):
                await self.playsong(ctx, self.musicQ[0])


    @commands.command(name='Queue', hidden=False)
    async def Queue(self, ctx):
        await ctx.send(self.musicQ)
    
    @commands.command(name='skip', hidden=False)
    async def skip(self, ctx):
        ctx.voice_client.stop()

    @commands.command(name='pause', hidden=False)
    async def stop(self, ctx):
        ctx.voice_client.pause()
    
    @commands.command(name='resume', hidden=False)
    async def resume(self, ctx):
        ctx.voice_client.resume()
            


async def setup(bot):
    await bot.add_cog(MusicCog(bot))