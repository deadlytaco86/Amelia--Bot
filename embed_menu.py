import discord
from discord.ext import commands

def addHelpFields(embed, i):
    embedfields = [
        [('ABOUT', f'I am a discord bot that was made primarly to play music without ads. My prefix is "." and if you ever need '
          f'the argument list for a command, just run the comamnd without any arguments. Try the command .help to get a '
          f'list of all the commands that I can do!'),
          ('SOURCE CODE','https://github.com/deadlytaco86/Amelia--Bot'),
          ('Page 1','Info'),
          ('Page 2','Music Commands'),
          ('Page 3','Math Commands'),
          ('Page 4','Graph Commands'),
          ('Page 5','Admin Commands'),
          ('Page 6','Pirate Commands'),
          ('Page 7','Egg Inc Commands')],

        [('.play', 'Enter keywords to find and play a specific song'),
         ('.play_random', 'Specify a folder and a random song will be played from it'),
         ('.pause', 'Pauses playback'),
         ('.resume', 'Resumes playback'),
         ('.skip', 'Skips the current song'),
         ('.stop', 'Stops the current song and clears the queue'),
         ('.leave', 'Leave the voice channel'),
         ('.queue', 'Lists all of the songs in the queue'),
         ('.songlist', 'lists all songs in a specified folder'),
         ('Available music folders', 'regular, ost, soundtrack, classical, christmas')],
        [('.add', 'Adds a list of numbers'),
         
         ('.sub', 'Subtracts a list of numbers from the first number'),
         ('.mult', 'Multiplies a list of numbers'),
         ('.div', 'Divides the first number by other numbers in the list'),
         ('.exp', 'Exponentiates a base by exponenet'),
         ('.log', 'Calculates log base any of a number'),
         ('.deriv','Calculate a derivative w.r.t x/y/z of f(x,y,z)'),
         ('.integ','Calculate the antiderivative of a function of x'),
         ('NOTE 1', 'For the above 2, type e^x as exp(x) \nFor function input, use X and not * because discord hates stars')],

        [('.pltpoly', 'Plots a polynomial from coefficients (include zeros)'),
         ('.plttxt', 'Plots data from an attahced text file with 1-3 columns'),
         ('.pltorbit', 'Creates an animation with given orbital parameters')],

        [('.kick', 'Kick someone'),
         ('.ban', 'Ban someone'),
         ('.clear', 'Clears messages'),
         ('.sleep', 'Puts the bot to sleep')],

        [('.ytsearch', 'Search query in youtube'),
         ('.download', 'Download a selection from the most recent search')],

        [('.register_egg_id', 'Register your EI number with the bot (include the EI part)'),
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
         ('.craft_odds', 'Shows you the odds of you crafting a LEG in the next n crafts'),
         ('.craftable', 'COMING SOON!'),
         ('DISCLAIMER!!!', 'Register your egg id at your own risk. The ids, which get encrypted \nwith the frenet library are stored in a json file on my personal computer.')]
    ]
    fields = embedfields[i]
    for name, value in fields:
        embed.add_field(name=name, value=value, inline=False)



class HelpMenu(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.embeds = [
            discord.Embed(title="1) INFO", description="--This is some basic bot information--", color=0xD718D4),
            discord.Embed(title="2) MUSIC", description="--This is a list of all MUSIC commands--", color=0xEEA228),
            discord.Embed(title="3) MATH", description="--This is a list of all MATH commands--", color=0xDFEF0E),
            discord.Embed(title="4) GRAPH", description="--This is a list of all GRAPH commands--", color=0x54f542),
            discord.Embed(title="5) ADMIN", description="--This is a list of all ADMIN commands--", color=0x0EEAEF),
            discord.Embed(title="6) PIRATE", description="--This is a list of all PIRATE commands--", color=0x0EEAEF),
            discord.Embed(title="7) EGG INC", description="--This is a list of all EGG INC commands--", color=0x0EEAEF)
        ]
        for i in range(7):
            addHelpFields(self.embeds[i], i)
        self.current_page = 0

    @discord.ui.button(label="Previous", style=discord.ButtonStyle.primary)
    async def previous_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            self.current_page = (self.current_page - 1) % len(self.embeds)
            await interaction.response.edit_message(embed=self.embeds[self.current_page])
        except:
            await interaction.followup.send("This menu is no longer active.", ephemeral=True)

    @discord.ui.button(label="Next", style=discord.ButtonStyle.primary)
    async def next_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_page = (self.current_page + 1) % len(self.embeds)
        await interaction.response.edit_message(embed=self.embeds[self.current_page])



class GraphMenu(discord.ui.View):
    def __init__(self, image_paths):
        super().__init__()
        self.image_paths = image_paths
        self.current_index = 0

    @discord.ui.button(label="Previous", style=discord.ButtonStyle.primary)
    async def previous_image(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_index = (self.current_index - 1) % len(self.image_paths)
        await self.update_image(interaction)

    @discord.ui.button(label="Next", style=discord.ButtonStyle.primary)
    async def next_image(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_index = (self.current_index + 1) % len(self.image_paths)
        await self.update_image(interaction)

    async def update_image(self, interaction: discord.Interaction):
        file_path = self.image_paths[self.current_index]
        file = discord.File(file_path, filename=file_path.split("/")[-1])
        await interaction.response.edit_message(attachments=[file])
