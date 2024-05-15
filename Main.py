from discord.ext.commands import has_permissions, MissingPermissions
from discord import FFmpegPCMAudio, member
from discord.ext import commands
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import date, datetime
from scipy.stats import binom
import discord, random, os
import asyncio
import numpy as np
import pandas as pd
from decimal import Decimal
import sympy as sym
import decimal
import base64
import json

from multiprocessing import Process

from orbit_animations import animate
from black_pearl import search, plunder
import ei_inventory_manager as eim

def check_folders() -> str: # this is in case anyone actually wants to use this bot.
    with open('bot_data/directories.txt', 'r') as f:
        directories = [direc.split('\n')[0] for direc in f.readlines()]

    for dir in directories:
        if not os.path.isdir(dir):
            os.mkdir(dir)
            print(f'created directory {dir}')
        else:
            print(f'found {dir}')
    
    print('a music folder path will have to be specified manually in the code as your file structure will be different from mine.')    

    current_directory = os.getcwd()
    return current_directory

def activate_bot(c_dir: str):

    #################
    ##### SETUP #####
    #################
        
    load_dotenv('keys.env')
    fernet = Fernet(os.getenv('ENCRYPTIONKEY'))

    client = commands.Bot(command_prefix='.', intents = discord.Intents.all())
    client.remove_command('help')

    decimal.getcontext().prec=60

    # for music
    m_dir = 'C:\\Desktop\\Ad free music for when AdBlock fails\\'
    queues = {}
    songs = []
    max_duplicate_iterations = 12

    ##################
    ##### EVENTS #####
    ##################

    @client.event
    async def on_ready():
        await client.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name="for commands"))
        print("Amelia is down to clown!")
        print("------------------------")
        #channel_general = client.get_channel(924502625590857768)
        #await channel_general.send("Good morning, I am back online")

    @client.event
    async def on_member_join(member):
        channel_general = client.get_channel(924502625590857768)
        role = discord.utils.get(member.guild.roles, name="citizen")
        await member.add_roles(role)
        await channel_general.send(str(member) + " has decided to come suffer with us")

    @client.event
    async def on_member_remove(member):
        channel_general = client.get_channel(924502625590857768)
        await channel_general.send(str(member) + " has decided that he could not take it any more")

    @client.event # floppa and wrong prefix
    async def on_message(message):
        if "floppa" in message.content.lower() or "secretbigkitty" in message.content.lower():
            if os.path.isfile('bot_data/bot_images/Bigfloppa.png'):
                image = discord.File("bot_data/bot_images/Bigfloppa.png")
                await message.channel.send(file=image)

        if "/help" in message.content.lower() or "!help" in message.content.lower():
            await message.channel.send('This bots prefix is "."\nTry using ".help"', reference=message)

        await client.process_commands(message)

    @client.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f'This command is on cooldown. Skipping too fast leads to errors')
            return
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send(f'missing arguments')
            return
        if isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send('whoops! looks like there was an error executing this command')
            raise error
            return
        #if isinstance(error, commands.CommandInvokeError):
            #print('clear command had a stupid error again')
            #print(error)
            #return
        else:
            raise error

    ######################
    ##### BASIC SHIT #####
    ######################

    @client.command()
    async def greet(ctx):
        await ctx.send("Salutations")

    @client.command()
    async def ping(ctx):
        await ctx.send("Pong")

    @client.command()
    async def info(ctx):
        await ctx.send(f'I am a discord bot that was made primarly to play music without ads. My prefix is "." and if you ever need '
                    f'the argument list for a command, just run the comamnd without any arguments. Try the command .help to get a '
                    f'list of all the commands that I can do!')

    @client.command()
    async def help(ctx):
        embed = discord.Embed(
            title='HELP MENU',
            description='--Navigate this menu to see all the commands--',
            color=0xD718D4
        )

        commands_list = [
            ('.help', 'Brings up this menu'),
            ('.music', 'Brings up a list of music commmands'),
            ('.math', 'Brings up a list of math commmands'),
            ('.graph', 'Brings up a list of graphing commmands'),
            ('.admin', 'Brings up a list of admin commmands'),
            ('.pirate', 'Brings up a list of pirating commmands'),
            ('.egg_inc', 'Brings up a list egg inc related commands'),
            ('.info', 'Brings up info about the bot')
        ]

        for name, value in commands_list:
            embed.add_field(name=name, value=value, inline=False)
        await ctx.send(embed=embed)

    @client.command()
    async def music(ctx):
        embed = discord.Embed(
            title='MUSIC COMMANDS',
            description='--This is a list of all music commands--',
            color=0xEEA228
        )

        commands_list = [
            ('.play', 'Enter keywords to find and play a specific song'),
            ('.play_random', 'Specify a folder and a random song will be played from it'),
            ('.pause', 'Pauses playback'),
            ('.resume', 'Resumes playback'),
            ('.skip', 'Skips the current song'),
            ('.stop', 'Stops the current song and clears the queue'),
            ('.leave', 'Leave the voice channel'),
            ('.queue', 'Lists all of the songs in the queue'),
            ('.songlist', 'lists all songs in a specified folder'),
            ('Available music folders', 'regular, ost, soundtrack, classical, christmas')
        ]

        for name, value in commands_list:
            embed.add_field(name=name, value=value, inline=False)
        await ctx.send(embed=embed)

    @client.command()
    async def math(ctx):
        embed = discord.Embed(
            title='MATH COMMANDS',
            description='--This is a list of all math commands--',
            color=0xDFEF0E
        )

        commands_list = [
            ('.add', 'Adds 2 numbers'),
            ('.sub', 'Subtracts 2 numbers'),
            ('.mult', 'Multiplies 2 numbers'),
            ('.div', 'Divides 2 numbers'),
            ('.exp', 'Exponentiates a base by exponenet'),
            ('.ln', 'Returns the natural log of a number'),
            ('.deriv','Calculate a derivative w.r.t x/y/z of f(x,y,z)'),
            ('.integ','Calculate the antiderivative of a function of x'),
            ('NOTE 1', 'For the above 2, type e^x as exp(x)'),
            ('NOTE 2', 'For function input, use X and not * because discord issues')
        ]

        for name, value in commands_list:
            embed.add_field(name=name, value=value, inline=False)
        await ctx.send(embed=embed)

    @client.command()
    async def graph(ctx):
        embed = discord.Embed(
            title='GRAPHING COMMANDS',
            description='--This is a list of all math commands--',
            color=0x54f542
        )

        commands_list = [
            ('.pltpoly', 'Plots a polynomial from coefficients (include zeors)'),
            ('.plttxt', 'Plots data from an attahced text file with 1-3 columns'),
            ('.pltorbit', 'Creates an animation with given orbital parameters')
        ]

        for name, value in commands_list:
            embed.add_field(name=name, value=value, inline=False)
        await ctx.send(embed=embed)

    @client.command()
    async def admin(ctx):
        embed = discord.Embed(
            title='ADMIN COMMANDS',
            description='--This is a list of all admin commands--',
            color=0x0EEAEF
        )

        commands_list = [
            ('.kick', 'Kick someone'),
            ('.ban', 'Ban someone'),
            ('.clear', 'Clears messages'),
            ('.sleep', 'Puts the bot to sleep')
        ]

        for name, value in commands_list:
            embed.add_field(name=name, value=value, inline=False)
        await ctx.send(embed=embed)

    @client.command()
    async def pirate(ctx):
        embed = discord.Embed(
            title='PIRATE COMMANDS',
            description='--This is a list of all pirating commands--',
            color=0x0EEAEF
        )

        commands_list = [
            ('.ytsearch', 'Search query in youtube'),
            ('.download', 'Download a selection from the most recent search')
        ]

        for name, value in commands_list:
            embed.add_field(name=name, value=value, inline=False)
        await ctx.send(embed=embed)

    @client.command()
    async def egg_inc(ctx):
        embed = discord.Embed(
            title='EGG INC COMMANDS',
            description='--This is a list of all egg inc commands--',
            color=0x0EEAEF
        )

        commands_list = [
            ('.register_egg_id', 'Register your EI number with the bot (include the EI part)'),
            ('.update_egg_inc', 'Update your egg inc inventory list'),
            ('.stats', 'Shows you some basic player stats (more stats in the future)'),
            ('.llc', 'Shows you your LLC'),
            ('.stone_report', 'Gives you the quantities and values of all your stones'),
            ('.ingredient_report', 'Gives you the quantities and values of all your ingredients'),
            ('.artifact_report', 'Gives you the quantities of all your artifacts (regardless of rarity)'),
            ('.archive', 'Archives your stone and ingredient quantities down to a 1 day resolution'),
            ('.history', 'enter the name of a stone or ingredient and its tier to see its quantity history'),
            ('.legs', 'Shows you a breakdown of all your legendary artifacts'),
            ('.shiny', '(IN DEV) shows you which shinies you have at a certain tier'),
            ('.guide', 'Brings up a guide on what artifacts to craft and consume'),
            ('.craftable', 'COMING SOON!'),
            ('DISCLAIMER!!!', 'Register your egg id at your own risk. The ids, which get encrypted \nwith the frenet library are stored in a json file on my personal computer.')
        ]

        for name, value in commands_list:
            embed.add_field(name=name, value=value, inline=False)
        await ctx.send(embed=embed)

    ###############################
    ####### ADMIN COMMANDS ########
    ###############################

    @client.command()
    @has_permissions(kick_members = True)
    async def kick(ctx, member: discord.Member, *, reason = None):
        await member.kick(reason = reason)
        await ctx.send(f'{member} has been deported!')

    @client.command()
    @has_permissions(ban_members = True)
    async def ban(ctx, member: discord.Member, *, reason = None):
        await member.ban(reason = reason)
        await ctx.send(f'{member} has been excommunicated!')

    @client.command()
    async def clear(ctx, *args):
        if len(args) != 1:
            await ctx.send("You need to provide a single intiger as your argument")
        elif ctx.author.guild_permissions.manage_messages:
            try:
                number = int(args[0]) + 1
                await ctx.channel.purge(limit=number)
            except:
                await ctx.send("Whoops, Looks like you entered a non integer or you tried to delete too many messages")
        else:
            await ctx.send("You don't have the necessary permissions to use this command.")

    @client.command()
    @has_permissions(administrator = True)
    async def promote(ctx, member: discord.Member):
        role = discord.utils.get(member.guild.roles, name="Supreme Chungus")
        await member.add_roles(role)
        await ctx.send(f'congradulations {member} on the promotion')

    @client.command()
    @has_permissions(administrator = True)
    async def demote(ctx, member: discord.Member):
        role = discord.utils.get(member.guild.roles, name="Supreme Chungus")
        await member.remove_roles(role)
        await ctx.send(f'{member} has been placed on administrative leave')

    @client.command(pass_content=True)
    async def fix_queue_error(ctx):
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        voice.stop()
        queues[ctx.guild.id] = []  # Clear the queue
        songs.clear()  # Clear the song names list

    @client.command()
    @has_permissions(administrator = True)
    async def sleep(ctx):
        await ctx.send("Good night!")
        await client.close()

    @kick.error
    async def kick_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have the permission to kick people")

    @ban.error
    async def ban_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have the permission to ban people")

    @promote.error
    async def promote_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have the permission to promote people")

    @demote.error
    async def demote_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have the permission to demote people")

    @sleep.error
    async def sleep_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have the permission to make the bot sleep")

    ###############################
    ##### VOICE CHANNEL STUFF #####
    ###############################

    @client.command()
    async def songlist(ctx, folder):
        available = ['regular', 'ost', 'soundtrack', 'classical', 'christmas']
        if folder not in available:
            await ctx.send(f'The music folder {folder} does not exist. Try another one')
            return
        folder_name = ['Every song', 'Game OST', 'Movie and Show themes', 'Classical', 'Christmas'][available.index(folder)]
        list = ['regular', 'game OST', 'soundtrack', 'classical', 'christmas'][available.index(folder)]
        directory = m_dir + folder_name + '\\'

        song_names = os.listdir(directory)
        with open("C://Desktop//Discord Bot//bot_data//music_files//song list.txt", 'w', encoding="utf-8") as p:
            for song in song_names:
                if song.endswith('.mp3') and song != "test1.mp3" and song != "test2.mp3":
                    p.write(song + "\n")

        current_date_str = date.today().strftime('%Y-%m-%d')
        current_time_str = datetime.now().strftime('%H:%M:%S')
        content = f'Here is the {list} song list as of {current_date_str}, {current_time_str}'
        await ctx.send(file = discord.File("C://Desktop//Discord Bot//bot_data//music_files//song list.txt"), content = content)
        os.remove("C://Desktop//Discord Bot//bot_data//music_files//song list.txt")

    @client.command(pass_content = True)
    async def join(ctx):
        if ctx.author.voice:
            channel_voice = ctx.message.author.voice.channel
            voice = await channel_voice.connect()
            ctx.bot.loop.create_task(disconnect_after_playing(ctx))
        else:
            await ctx.send("You have to be in a voice channel to use this command")

    @client.command(pass_content=True)
    async def play(ctx, *args):
        if len(args) == 0:
            await ctx.send('You need to give some keywords to search with')
            return
        ##### get a list of every song #####
        directories = []
        for path in os.listdir(m_dir):
            if '.' not in path and 'visible' not in path:
                directories.append(path)
        songlist = []
        for path in directories:
            songlist += [path + '\\' + song for song in os.listdir(m_dir + path)]
        
        ##### get all the keywords #####
        keywords = []
        for i in range(len(args)):
            keywords.append(str(args[i]))
        keys = len(keywords)
        key_count = 0
        while len(songlist) > 1 and key_count < keys:
            songlist = narrow_down(songlist, keywords[key_count])
            key_count += 1

        if len(songlist) == 0:
            await ctx.send('no results found. loosen your search')
            return
        if len(songlist) > 1:
            await ctx.send('more than 1 result found. use more keywords')
            return
        else:
            audio_name = songlist[0]

        voice_state = ctx.author.voice
        if voice_state is None:
            await ctx.send("You are not connected to a voice channel.")
            return

        voice_channel = voice_state.channel
        voice_client = ctx.voice_client

        if voice_client is None:
            voice = await voice_channel.connect()

        if voice_client and voice_client.is_playing():
            source = FFmpegPCMAudio(m_dir + str(audio_name))
            songs.append(audio_name)
            guild_id = ctx.guild.id

            if guild_id in queues:
                queues[guild_id].append(source)
            else:
                queues[guild_id] = [source]
            await ctx.send(f'Added to queue')

        else:
            voice = ctx.guild.voice_client
            source = FFmpegPCMAudio(m_dir + str(audio_name))
            try:
                player = voice.play(source, after=lambda e, gid=ctx.guild.id: check_queue(ctx, gid))
                if player:
                    player.after = None
            except Exception as e:
                await ctx.send(f"Error playing the song: {str(e)}")

    @client.command(pass_content=True)
    async def play_random(ctx, folder=None, quantity=None):
        if quantity == None: # do some argument checks
            quantity = 1
        else:
            quantity = int(quantity)
        if quantity > 40:
            quantity = 40
            await ctx.send('to avoid overloading the queue, only 40 songs will be randomly chosen and added to queue at a time')
        if folder == None:
            await ctx.send('missing arguments: <folder> optional: <number of random songs>')
            return
        
        available = ['regular', 'ost', 'soundtrack', 'classical', 'christmas']
        if folder not in available:
            await ctx.send(f'The music folder {folder} does not exist. Try another one')
            return
        folder_name = ['Every song', 'Game OST', 'Movie and Show themes', 'Classical', 'Christmas'][available.index(folder)]
        directory = m_dir + folder_name + '\\'

        voice_state = ctx.author.voice
        if voice_state is None:
            await ctx.send("You are not connected to a voice channel.")
            return
        
        voice_channel = voice_state.channel
        voice_client = ctx.voice_client

        if voice_client is None:
            voice = await voice_channel.connect()

        all_songs = os.listdir(directory)
        random_choice = random.choice(all_songs)
        iterations = 0
        while random_choice in songs and iterations < max_duplicate_iterations:
            random_choice = random.choice(all_songs)
            iterations += 1

        source = FFmpegPCMAudio(directory + str(random_choice))
        guild_id = ctx.guild.id
        if voice_client and voice_client.is_playing():
            songs.append(random_choice)
            if guild_id in queues:
                queues[guild_id].append(source)
            else:
                queues[guild_id] = [source]
            await ctx.send(f'Added to queue')

        else:
            voice = ctx.guild.voice_client
            try:
                player = voice.play(source, after=lambda e, gid=guild_id: check_queue(ctx, gid))
                if player:
                    player.after = None
            except Exception as e:
                await ctx.send(f"Error playing the song: {str(e)}")

        if quantity > 1:
            for i in range(quantity - 1):
                random_choice = random.choice(all_songs)
                iterations = 0
                while random_choice in songs and iterations < max_duplicate_iterations:
                    random_choice = random.choice(all_songs)
                    iterations += 1
                source = FFmpegPCMAudio(directory + str(random_choice))
                songs.append(random_choice)
                if guild_id in queues:
                    queues[guild_id].append(source)
                else:
                    queues[guild_id] = [source]

    def narrow_down(remaining_songs, key):
        results = []
        for name in remaining_songs:
            if key.lower() in name.lower():
                results.append(name)
        return results

    def check_queue(ctx, guild_id):
        if guild_id in queues:
            if len(queues[guild_id]) > 0:
                voice = ctx.guild.voice_client
                source = queues[guild_id].pop(0)
                songs.pop(0)
                player = voice.play(source, after=lambda e, gid=guild_id: check_queue(ctx, gid))

                if player:
                    player.after = None
            else:
                ctx.bot.loop.create_task(disconnect_after_playing(ctx))
        else:
            ctx.bot.loop.create_task(disconnect_after_playing(ctx))

    async def disconnect_after_playing(ctx):
        await asyncio.sleep(10)

        voice_client = ctx.guild.voice_client
        if voice_client and voice_client.is_playing():
            return

        if voice_client and voice_client.is_connected():
            await voice_client.disconnect()
        else:
            return

    @client.command(pass_content = True)
    async def pause(ctx):
        voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
        if voice.is_playing():
            voice.pause()
        else:
            await ctx.send("The audio is already paused")

    @client.command(pass_content = True)
    async def resume(ctx):
        voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
        if voice.is_paused():
            voice.resume()
        else:
            await ctx.send("The audio is already playing")

    @client.command(pass_content=True)
    @commands.cooldown(1, 1.5, commands.BucketType.guild)
    async def skip(ctx):
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

        if voice and voice.is_playing():
            voice.stop()
            await ctx.send("Skipping the current song.")
        else:
            await ctx.send("The bot is not currently playing anything.")

        # Remove the current song from the queue and songs list
        guild_id = ctx.guild.id
        if guild_id in queues and len(queues[guild_id]) > 0:
            return
        else:
            await ctx.send("There are no more songs in the queue.")

    @client.command(pass_content=True)
    async def stop(ctx):
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

        if voice and voice.is_playing():
            voice.stop()
            queues[ctx.guild.id] = []  # Clear the queue
            songs.clear()  # Clear the song names list
            await ctx.send("Playback stopped and queue cleared.")
        else:
            await ctx.send("The bot is not currently playing anything.")

    @client.command(pass_context=True)
    async def leave(ctx):
        voice_client = ctx.guild.voice_client

        if voice_client:
            guild_id = ctx.guild.id
            if guild_id in queues:
                queues.pop(guild_id)  # Clear the queue for the current guild
            await voice_client.disconnect()
        else:
            await ctx.send("I am not in a voice channel.")

    @client.command(pass_content = True)
    async def queue(ctx):
        guild_id = ctx.message.guild.id

        if guild_id in queues and queues[guild_id]:
            embed = discord.Embed(
                title='Queue',
                description='List of songs in the queue:',
                color=discord.Color.blue()
            )

            songs_cleaned = []
            count = 1
            backslash = '\\'
            for song in songs:
                songs_cleaned.append(f'{count}. {song.split(backslash)[1] if backslash in song else song}')

            embed.add_field(name='up next...', value='\n'.join(songs_cleaned), inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send('The queue is empty.')

    #######################
    ##### SIMPLE MATH #####
    #######################

    @client.command()
    async def mult(ctx, arg1 = None, arg2= None):
        if arg1 == None or arg2 == None:
            await ctx.send("You are missing some arguments: <first number> <second number>")
        else:
            await ctx.send(Decimal(arg1)*Decimal(arg2)) # ctx.send(float(arg1)*float(arg2))

    @client.command()
    async def div(ctx, arg1 = None, arg2= None):
        if arg1 == None or arg2 == None:
            await ctx.send("You are missing some arguments: <numerator> <denominator>")
        elif Decimal(arg2) == 0:
            await ctx.send("Pease don't make me devide by zero")
        else:
            await ctx.send(Decimal(arg1)/Decimal(arg2))

    @client.command()
    async def add(ctx, arg1 = None, arg2= None):
        if arg1 == None or arg2 == None:
            await ctx.send("You are missing some arguments: <first number> <second number>")
        else:
            await ctx.send(Decimal(arg1)+Decimal(arg2))

    @client.command()
    async def sub(ctx, arg1 = None, arg2= None):
        if arg1 == None or arg2 == None:
            await ctx.send("You are missing some arguments: <first number> <second number>")
        else:
            await ctx.send(Decimal(arg1)-Decimal(arg2))

    @client.command()
    async def exp(ctx, arg1 = None, arg2= None):
        if arg1 == None or arg2 == None:
            await ctx.send("You are missing some arguments: <base> <exponenet>")
        else:
            await ctx.send(Decimal(arg1)**Decimal(arg2))

    @client.command()
    async def ln(ctx, arg1 = None):
        if arg1 == None:
            await ctx.send("You are missing an argument: <base> <number>")
        else:
            await ctx.send(np.log(arg1))

    @client.command()
    async def dice(ctx, n = None, k = None, p = None):
        if n == None or k == None or p == None:
            await ctx.send("missing arguments")
            return
        await ctx.send(f'probability of {k}/{n} is {100 - np.round(100*binom.cdf(int(k) - 1, int(n), 1/int(p)), 5)}')
    
    @client.command()
    async def deriv(ctx, *args):
        if len(args) <= 1:
            await ctx.send('.deriv <w.r.t x/y/z> <funtion of x> (note write e^x as exp(x))')
            return
        x, y, z = sym.symbols('x y z')
        w_r_t = args[0]
        expression = ' '.join(args[1:])
        replaced = "*".join(str(expression).split("X"))

        derivative = sym.diff(replaced, w_r_t) # w_r_t
        double_filt = "^".join(str(derivative).split("**"))
        single_filt = "".join(str(double_filt).split("*"))
        await ctx.send(f'd/d{w_r_t} is: {single_filt}')

    @client.command()
    async def integ(ctx, *args):
        if len(args) == 0:
            await ctx.send('.integ <funtion of x> (note write e^x as exp(x))')
            return

        x, y = sym.symbols('x y')
        expression = ' '.join(args)
        replaced = "*".join(str(expression).split("X"))

        integral = sym.integrate(replaced, x)
        double_filt = "^".join(str(integral).split("**"))
        single_filt = "".join(str(double_filt).split("*"))
        #print(str(derivative))
        await ctx.send(f'integral of y(x) is: {single_filt} + C')

    ####################
    ##### Graphing #####
    ####################

    @client.command()
    async def pltpoly(ctx, *args):
        if len(args) < 3:
            await ctx.send("You are missing some arguments: <start> <end> <coefficient 1> ... <coefficient n>")
        else:
            try:
                degree = len(args) - 3
                x1 = float(args[0])
                x2 = float(args[1])
                span = x2 - x1
                points = int(span*20)
                x = np.linspace(x1,x2,points)
                y = np.zeros(len(x))
                for i in range(degree + 1):
                    y += float(args[i+2])*x**(degree-i)
                plt.plot(x,y,'b-')
                plt.grid(which='major', color='#DDDDDD', linewidth=0.8)
                plt.grid(which='minor', color='#EEEEEE', linewidth=0.5)
                plt.minorticks_on()
                plt.title("Your polynomial Graph")
                plt.xlabel("X axis")
                plt.ylabel("Y axis")
                plt.savefig("C://Desktop//Discord Bot//bot_data//graph_data//graph.png")
                plt.close()
                image = discord.File("C://Desktop//Discord Bot//bot_data//graph_data//graph.png")
                await ctx.send(file=image)
            except:
                await ctx.send('Could not make the graph. Please input only numbers.')

    @client.command()
    async def plttxt(ctx, *args):
        params = len(args)
        if params < 3:
            await ctx.send('You are missing some arguments: <"data seris name"> <"x label"> <"y label"> optional: <dot>')
        else:
            if len(ctx.message.attachments) == 0:
                await ctx.send("You need to attach a text file")
                return
            
            attachment = ctx.message.attachments[0]
            if attachment.content_type.startswith("text/plain"): 
                file_contents = await attachment.read()
                file_contents = file_contents.decode("utf-8")
                with open('C://Desktop//Discord Bot//bot_data//graph_data//txt_data.txt','w') as p:
                    p.write(file_contents)
                data = np.loadtxt('C://Desktop//Discord Bot//bot_data//graph_data//txt_data.txt')

                if len(data.shape) == 1:
                    if params == 3:
                        plt.plot(data,'b-')
                    else:
                        plt.plot(data, 'b.')

                elif data.shape[1] == 2:
                    if params == 3:
                        plt.plot(data[:,0],data[:,1],'b-')
                    else:
                        plt.plot(data[:,0],data[:,1],'b.')

                elif data.shape[1] == 3:
                    if params == 3:
                        plt.errorbar(data[:,0],data[:,1], yerr=data[:,2], fmt='o', ecolor='black', elinewidth=0.6, color='blue', capsize=3.5)
                        plt.plot(data[:,0],data[:,1],'b-')
                    else:
                        plt.errorbar(data[:,0],data[:,1], yerr=data[:,2], fmt='o', ecolor='black', elinewidth=0.6, color='blue', capsize=3.5)

                plt.grid(which='major', color='#DDDDDD', linewidth=0.8)
                plt.grid(which='minor', color='#EEEEEE', linewidth=0.5)
                plt.minorticks_on()
                plt.title(args[0])
                plt.xlabel(args[1])
                plt.ylabel(args[2])
                plt.savefig("C://Desktop//Discord Bot//bot_data//graph_data//graph.png")
                plt.close()
                image = discord.File("C://Desktop//Discord Bot//bot_data//graph_data//graph.png")
                await ctx.send(file=image)
        
            else:
                await ctx.send("The attached file is not a text file.")

    async def pltorbit_thread(ctx, *args):
        if len(args) < 3:
            await ctx.send("missing arguments: <eccentricity> <radius (AU)> <mass (solar masses)>")
            return
        if float(args[0]) < 0.0 or float(args[0]) >= 1.0:
            await ctx.send("Eccentricity must be positive but cannot be one or greater")
            return
        else:
            message = await ctx.send('This will take a few seconds...')
            try:
                loop = asyncio.get_event_loop()
                await loop.run_in_executor(None, animate, float(args[0]), float(args[1]), float(args[2]))
                image = discord.File('C://Desktop//Discord Bot//bot_data//graph_data//Orbit Animation.gif')
                await message.delete()
                await ctx.send(file=image)
            except Exception as e:
                await message.delete()
                await ctx.send('There was an error making your plot')

    @client.command()
    async def pltorbit(ctx, *args):
        future = asyncio.ensure_future(pltorbit_thread(ctx, *args))
        await future


    ####################
    ##### PIRATING #####
    ####################
                
    @client.command()
    async def ytsearch(ctx, *args):
        if len(args) == 0:
            await ctx.send('missing arguments: <search query>')
            return
        else:
            #print(f'searching for {" ".join(args)}')
            message = await ctx.send('Working...')
            search_results = search(' '.join(args), 1)

            urls = []
            titles = []
            authors = []
            durations = []
            publish_dates = []

            for result in search_results.results:

                urls.append(result.video_id)
                #print(result.thumbnail_url)

                titles.append(result.title)
                authors.append(result.author)
                publish_dates.append(str(result.publish_date).split('00')[0])

                length = result.length
                hours = length // 3600
                buffer_1 = '0' if len(str(hours)) == 1 else ''
                minutes = (length - hours*3600) // 60
                buffer_2 = '0' if len(str(minutes)) == 1 else ''
                seconds = (length - hours*3600 - minutes*60)
                buffer_3 = '0' if len(str(seconds)) == 1 else ''
                durations.append(f'{buffer_1}{hours}:{buffer_2}{minutes}:{buffer_3}{seconds}')

                #print(f'{index}. {title} --- {author} --- {duration} --- {publish_date}')

            with open("C://Desktop//Discord Bot//bot_data//music_files//search_results.txt", 'w', encoding="utf-8") as p:
                for id in urls:
                    p.write(id + "\n")

            embed = discord.Embed(
                title='Search results',
                description='Results from the most recent youtube search:',
                color=discord.Color.blue()
            )

            for index, result in enumerate(search_results.results, start=1):
                embed.add_field(name=f'{index}. {titles[index-1]}', value=f'{authors[index-1]} --- {durations[index-1]} --- {publish_dates[index-1]}', inline=False)

            await message.delete()
            await ctx.send(embed=embed)
            await ctx.send('ready to download a selection or search again')

    @client.command()
    async def download(ctx, arg1 = None, arg2 = None):
        if arg1 == None:
            await ctx.send('missing arguments: <song number> optional: <folder>')
            return
        try:
            selection = int(arg1)
        except:
            await ctx.send('selection must match one of the numbers of the search result')
            return
        
        with open("C://Desktop//Discord Bot//bot_data//music_files//search_results.txt", 'r') as p:
            ids = p.readlines()
            try:
                if arg2 == None or arg2 not in ['regular', 'ost', 'soundtrack', 'classical', 'christmas']:
                    await ctx.send('folder not recognized, re-routing to default folder instead')
                    plunder(str(ids[selection-1]).split('\n')[0])
                else:
                    plunder(str(ids[selection-1]).split('\n')[0], arg2)
                await ctx.send('Download complete!')
            except:
                await ctx.send('Something went wrong. Check to make sure you do not already have this item.')

    ####################
    ##### EGG INC ######
    ####################

    @client.command()
    async def register_egg_id(ctx, id=None):
        if id == None:
            await ctx.send('missing arguments: <EI################>')
            return
        if 'EI' not in id:
            id = 'EI' + id
        if len(id) - 2 != 16:
            await ctx.message.delete()
            await ctx.send('there should be 16 numbers after the EI. Make sure you have all of them')
            return
        f = open('C://Desktop//Discord Bot//bot_data//egg_inc_data//ei_registered_ids.json')
        ids = json.load(f)
        user = str(ctx.author)
        if user in ids:
            await ctx.message.delete()
            await ctx.send('you have already registered your egg inc id')
        else:
            try:
                encrypted_id = fernet.encrypt(id.encode())
                encrypted_id_base64 = base64.b64encode(encrypted_id).decode()
                ids[user] = encrypted_id_base64
                json_object = json.dumps(ids, indent=4)
                with open('C://Desktop//Discord Bot//bot_data//egg_inc_data//ei_registered_ids.json', 'w') as writer:
                    writer.write(json_object)
                await ctx.message.delete()
                await ctx.send('your egg inc id is now registered with the bot!')
            except:
                await ctx.message.delete()
                await ctx.send('registration failed')
        f.close()

    @client.command()
    async def update_egg_inc(ctx):
        user = str(ctx.author)
        have_id, enc_id = eim.verify_prereqs(user)
        if not have_id:
            await ctx.send('you need to register your id with the bot first with ".register_egg_id <id>"')
            return
        else:
            user_id = fernet.decrypt(base64.b64decode(enc_id)).decode()
            eim.get_full_inventory(user, user_id)
            eim.sort_by_name(user)
            await ctx.send('Artifact inventory is now up to date')

    @client.command()
    async def stats(ctx):
        user = str(ctx.author)
        stats_list = eim.stat_list(user)

        if stats_list == None:
            await ctx.send('please run .update_egg_inc first in order to generate a stats file')
            return

        embed = discord.Embed(
            title='Player Stats',
            description='--This is a list of your basic game stats--',
            color=0x009933
        )

        embed.add_field(name=f'Here are your basic game stats...', value=f'```{stats_list}```', inline=False)
        await ctx.send(embed=embed)

    @client.command()
    async def llc(ctx):
        user = str(ctx.author)
        have_id, enc_id = eim.verify_prereqs(user)
        if not have_id:
            await ctx.send('you need to register your id with the bot first with ".register_egg_id <id>"')
            return
        else:
            user_id = fernet.decrypt(base64.b64decode(enc_id)).decode()
            llc_text = eim.get_llc(user_id)

            embed = discord.Embed(
                title='Here is your LLC report...',
                description='',
                color=0x42f5d4
            )

            embed.add_field(name=f'', value=f'{llc_text}', inline=False)
            await ctx.send(embed=embed)

    @client.command()
    async def view_raw_inventory(ctx):
        user = str(ctx.author)
        if os.path.isfile(f'C://Desktop//Discord Bot//bot_data//egg_inc_data//{user}_all artifacts.json'):
            await ctx.send(file = discord.File(f'C://Desktop//Discord Bot//bot_data//egg_inc_data//{user}_all artifacts.json'))
        else:
            await ctx.send('no artifact record exists for you yet. please run ".update_egg_inc" to create one')
        
    @client.command()
    async def stone_report(ctx):
        user = str(ctx.author)
        stone_list = eim.make_stone_list(user)

        if stone_list == None:
            await ctx.send('please run .update_egg_inc first in order to generate an artifact file')
            return

        embed = discord.Embed(
            title='Stone Report',
            description='--This is a list of all your stones and fragments--',
            color=0x0EEAEF
        )

        for name, value in stone_list:
            embed.add_field(name=name, value=value, inline=False)
        await ctx.send(embed=embed)    

    @client.command()
    async def ingredient_report(ctx):
        user = str(ctx.author)
        ingredient_list = eim.make_ingredient_list(user)

        if ingredient_list == None:
            await ctx.send('please run .update_egg_inc first in order to generate an artifact file')
            return

        embed = discord.Embed(
            title='Ingredient Report',
            description='--This is a list of all your ingredients--',
            color=0x0EEAEF
        )

        for name, value in ingredient_list:
            embed.add_field(name=name, value=value, inline=False)
        await ctx.send(embed=embed)    

    @client.command()
    async def artifact_report(ctx):
        user = str(ctx.author)
        artifact_list = eim.make_artifact_list(user)

        if artifact_list == None:
            await ctx.send('please run .update_egg_inc first in order to generate an artifact file')
            return

        embed = discord.Embed(
            title='Artifact Report',
            description='--This is a list of all your artifacts--',
            color=0x0EEAEF
        )

        for name, value in artifact_list:
            embed.add_field(name=name, value=value, inline=False)
        await ctx.send(embed=embed)

    @client.command()
    async def legs(ctx):
        user = str(ctx.author)
        legs_list, total = eim.legendary_list(user)

        if legs_list == None:
            await ctx.send('please run .update_egg_inc first in order to generate an artifact file to pull legs from')

            return

        embed = discord.Embed(
            title='LEGENDARY Report',
            description='--This is a list of all your LEGENDARY artifacts--',
            color=0xffff00
        )

        embed.add_field(name=f'Here is a breakdown of your {total} LEGENDARY artifacts...', value=f'```{legs_list}```', inline=False)
        await ctx.send(embed=embed)

    @client.command()
    async def shiny(ctx, tier=None):
        if tier == None:
            await ctx.send('You need to enter a tier. eg: .shiny <1 or t1 or T1>')
            return
        if tier.upper() not in ['1', '2', '3', '4', 'T1', 'T2', 'T3', 'T4']:
            await ctx.send('Please enter a valid tier, 1 through 4. eg: .shiny <1 or t1 or T1>')
            return
        if len(tier) == 1:
            tier = f'T{tier}'
            tier_num = int(tier[-1])
        else:
            tier = tier.upper()
            tier_num = int(tier[-1])

        user = str(ctx.author)
        shiny_list= eim.shiny_list(user, tier)

        if shiny_list == None:
            await ctx.send('please run .update_egg_inc first in order to generate an artifact file')
            return

        embed = discord.Embed(
            title='Shiny Report',
            description=f'--This is a list of all your Tier {tier_num} SHINY artifacts--',
            color=0xffff00
        )

        embed.add_field(name=f'Here is a breakdown of Tier {tier_num} shiny artifacts...', value=f'```{shiny_list}```', inline=False)
        await ctx.send(embed=embed)
    
    @client.command()
    async def archive(ctx):
        user = str(ctx.author)
        current_date_str = date.today().strftime('%Y-%m-%d')
        return_code = eim.create_archive_entry(user, current_date_str)
        if return_code == 1:
            ctx.send('you need to update your inventory with .update_egg_inc before you can run this command')
            return
        await ctx.send(f'Entry created for {current_date_str}')
    
    @client.command()
    async def guide(ctx):
        image = discord.File("bot_data/bot_images/guide.png")
        await ctx.send(file=image)

    @client.command()
    async def history(ctx, *args):
        user = str(ctx.author)
        if not os.path.isfile(f'C://Desktop//Discord Bot//bot_data//egg_inc_data//archives//{user}_history.json'):
            await ctx.send('you do not have any artifact history, you can create onw with .archive after every inventory update')
            return
        else:
            with open(f'C://Desktop//Discord Bot//bot_data//egg_inc_data//archives//{user}_history.json', 'r') as f:
                history = json.load(f)
            artifact = (' '.join(args)).upper()
            if eim.check_valid_artifact(artifact):
                x = [date for date in history]
                x = pd.to_datetime(x)
                y = [history[date][artifact] for date in history]

                plt.rcParams["figure.figsize"] = (8,4.5)
                plt.plot_date(x, y, 'g--')
                plt.title(f"{user}'s {artifact} history")
                #plt.xlabel('Dates')
                plt.ylabel('Quantity')
                plt.xticks(rotation=40)
                plt.grid(which='major', color='#DDDDDD', linewidth=0.8)
                #plt.grid(which='minor', color='#EEEEEE', linewidth=0.5)
                #plt.minorticks_on()
                plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
                plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=3))
                plt.tight_layout(pad=1.5)
                plt.savefig(f"C://Desktop//Discord Bot//bot_data//egg_inc_data//{user}_history.png") #  bbox_inches="tight"
                plt.clf()

                image = discord.File(f"C://Desktop//Discord Bot//bot_data//egg_inc_data//{user}_history.png")
                await ctx.send(file=image)
                os.remove(f"C://Desktop//Discord Bot//bot_data//egg_inc_data//{user}_history.png")
            else:
                await ctx.send(f'{artifact} is not in the archives. Please ensure you are selecting a stone or ingredient and spelling is correct.')
                return
    
    @client.command()
    async def craftable(ctx, *args):
        send_embed = False
        user = str(ctx.author)
        if not os.path.isfile(f'C://Desktop//Discord Bot//bot_data//egg_inc_data//{user}_quantity data.json'):
            await ctx.send('you do not have an inventory on record. Please run .update_egg_inc to create one.')
            return
        else:
            artifact = (' '.join(args)).upper()
            tree, available = eim.craft(artifact, user)

            if tree == None:
                await ctx.send('looks like you spelled something wrong')
                return

            if send_embed:
                embed = discord.Embed(
                    title=f'Crafting a {artifact}',
                    description='Here is what you will DIRECTLY need:',
                    color=0x0EEAEF
                )

                for name, value in tree:
                    embed.add_field(name=name, value=value, inline=False)
                await ctx.send(embed=embed)
            else:
                with open('crafting_tree.txt', 'w') as f:
                    for item in tree:
                        f.write(str(item)+'\n')
                    f.write('\n')
                    for item in available:
                        f.write(f'you have {available[item]} {item}\n')

                file = discord.File("C://Desktop//Discord Bot//crafting_tree.txt")
                await ctx.send(file=file)


    ####################
    ##### RUN BOT ######
    ####################

    client.run(os.getenv('BOTTOKEN'))

if __name__ == "__main__":
    c_dir = check_folders()
    activate_bot(c_dir)

# see that can be done with this: https://replit.com/@Brosssh/NEW-LLC-CALCULATOR#main.py
# https://github.com/DavidArthurCole/EggLedger/releases
# https://eggincdatacollection.azurewebsites.net/api/GetLLCData
# https://lunarstige--wasmegg-carpet.netlify.app/smart-assistant
# https://github.com/menno-egginc/eggincdatacollection-docs/blob/main/DataEndpoints.md
# https://github.com/menno-egginc/egg/tree/main/protobuf
# https://inicio-multi.netlify.app/

