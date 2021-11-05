import discord
from discord.ext import commands
import youtube_dl
#PyNaCl must also be installed
#Must also have ffmpeg.exe, ffplay.exe, and ffprobe.exe in the path folder

TOKEN = 'your bot token'

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=commands.when_mentioned_or("."), intents=intents, help_command=None)

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.command(pass_context = True)
async def join(ctx):
    if (ctx.author.voice):
        if (ctx.voice_client):
            await ctx.send("I already joined")
        else:
            channel = ctx.message.author.voice.channel
            await channel.connect()
    else:
        await ctx.send("Join a voice channel first")

@bot.command(pass_context = True)
async def play(ctx, url):
    joined = False

    if (ctx.author.voice):
        if (ctx.voice_client):
            joined = True
        else:
            channel = ctx.message.author.voice.channel
            joined = True
            await channel.connect()
    else:
        await ctx.send("Join a voice channel first")

    if joined == True:
        username = str(ctx.author).split('#')[0]
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                          'options': '-vn'}
        YDL_OPTIONS = {'format': 'bestaudio'}
        vc = ctx.voice_client
        await ctx.send(f'Playing Music for {username}.')
        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
            vc.play(source)

@bot.command(pass_context = True)
async def pause(ctx):
    if (ctx.author.voice):
        if (ctx.voice_client):
            ctx.guild.voice_client.pause()
            await ctx.send("Paused")
        else:
            await ctx.send("I'm not playing music.")
    else:
        await ctx.send("Join a voice channel first")

@bot.command(pass_context = True)
async def resume(ctx):
    if (ctx.author.voice):
        if (ctx.voice_client):
            ctx.guild.voice_client.resume()
            await ctx.send("Resumed")
        else:
            await ctx.send("I'm not playing music.")
    else:
        await ctx.send("Join a voice channel first")

@bot.command(pass_context = True)
async def stop(ctx):
    if (ctx.author.voice):
        if (ctx.voice_client):
            ctx.guild.voice_client.stop()
            await ctx.send("Stopped")
            await ctx.guild.voice_client.disconnect()
        else:
            await ctx.send("I'm not playing music.")
    else:
        await ctx.send("Join a voice channel first")

@bot.command(pass_context = True)
async def skip(ctx):
    if (ctx.author.voice):
        if (ctx.voice_client):
            ctx.guild.voice_client.stop()
            await ctx.send("Skipped")
        else:
            await ctx.send("I'm not playing music.")
    else:
        await ctx.send("Join a voice channel first")

bot.run(TOKEN)