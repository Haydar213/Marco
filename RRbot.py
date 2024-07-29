import asyncio
import discord
from discord.ext import commands, tasks
from discord import Game, Status, Activity, ActivityType
import random
import json
import os


# Global Variables
cooldown_seconds = 5
last_user = None
current_number = 1
mistake_count = 0
max_mistakes = 3

intents = discord.Intents.all()
intents.members = True
intents.messages = True
intents.reactions = True

client = commands.Bot(command_prefix='!', intents=intents)

StreamChennel = 1090982004054569051
counting_channel_id = 1157844394758639708

script_directory = os.path.dirname(os.path.realpath(__file__))
filename = os.path.join(script_directory, 'counting_data.json')
emoji_file_path = os.path.join(script_directory, 'custom_emojis.json')
current_number = 1
try:
    with open(filename, 'r') as file:
        data = json.load(file)
        current_number = data.get('current_number', 1)
except FileNotFoundError:
    pass

emoji_role_dict = {
                "<:hehim:1091554851495882905>": 'He/Him',
                "<:sheher:1091554853798563901>": 'She/Her',
                "<:18:1091554850216624189>": '18+',
                "<:corgartist:1091554863202185339>": 'Artist',
                "<:tayguitar:1091559548650795108>": 'Musician',
                "<:valo:1091557705048653876>": 'Valorant',
                "<:minecraft:1091554887927611533>": 'Minecraft',
                "<:genshin:1091555382326997072>": 'Genshin',
                "<:gta:1091554857346936902>": 'GTA',
                "<:csgo:1091554884098199632>": 'CSGO',
                "<:roblox:1091543997652148364>": 'Roblox',
                "<:fortnite:1091555927267754004>": 'Fortnite',
                "<:iron:1091554858773004328>": 'Iron',
                "<:bronze:1091554870668054558>": 'Bronze',
                "<:silver:1091554867832692816>": 'Silver',
                "<:gold:1091554865605517342>": 'Gold',
                "<:plat:1091555554469625867>": 'Platinum',
                "<:dia:1091555726771617822>": 'Diamond',
                "<:asc:1091554860979191819>": 'Ascendant',
                "<:imm:1091554875143364640>": 'Immortal',
                "<:radiant:1091554877450227774>": 'Radiant',
                "<:twitch:1091554880117813269>": 'Streamer',
                "<:less18:1091881733609230346>": 'Minor',
                "<:theythem:1091881243265744946>": 'They/Them',
                "<:weebster:1091760142493700167>": 'Weeb',
                "<:jinxlol:1092484411108376686>": 'LoL',
                "<:apex:1091554854863896588>": 'Apex',
                "<:watamelon:1117044520354332703>": 'Honkai SR',
                "<:derpykayo:1096138908636561571>": 'Stream'
}
general_emoji_dict = {
    "<:hehim:1091554851495882905>": 'He/Him',
    "<:sheher:1091554853798563901>": 'She/Her',
    "<:theythem:1091881243265744946>": 'They/Them',
    "<:18:1091554850216624189>": '18+',
    "<:less18:1091881733609230346>": 'Minor',
    "<:corgartist:1091554863202185339>": 'Artist',
    "<:tayguitar:1091559548650795108>": 'Musician',
    "<:twitch:1091554880117813269>": 'Streamer',
    "<:weebster:1091760142493700167>": 'Weeb'
}
game_emoji_dict = {
    "<:valo:1091557705048653876>": 'Valorant',
    "<:minecraft:1091554887927611533>": 'Minecraft',
    "<:genshin:1091555382326997072>": 'Genshin',
    "<:gta:1091554857346936902>": 'GTA',
    "<:csgo:1091554884098199632>": 'CSGO',
    "<:roblox:1091543997652148364>": 'Roblox',
    "<:fortnite:1091555927267754004>": 'Fortnite',
    "<:jinxlol:1092484411108376686>": 'LoL',
    "<:apex:1091554854863896588>": 'Apex',
    "<:watamelon:1117044520354332703>": 'Honkai SR'
}
rank_emoji_dict = {
    "<:iron:1091554858773004328>": 'Iron',
    "<:bronze:1091554870668054558>": 'Bronze',
    "<:silver:1091554867832692816>": 'Silver',
    "<:gold:1091554865605517342>": 'Gold',
    "<:plat:1091555554469625867>": 'Platinum',
    "<:dia:1091555726771617822>": 'Diamond',
    "<:asc:1091554860979191819>": 'Ascendant',
    "<:imm:1091554875143364640>": 'Immortal',
    "<:radiant:1091554877450227774>": 'Radiant'
}
stream_emoji_dict = {
    "<:derpykayo:1096138908636561571>": 'Stream'

}

STREAMER_ROLE_NAME = 'Streamer'

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
message_ids = [
    1091882440089415710,
    1091882503377277098,
    1091882551498526811,
    1123935617449984010
]

@client.command(name='ranklist', help='Shows the list of available roles')
async def rank_list(ctx):
    embed = discord.Embed(title='Ranks List', description='React to the corresponding emoji to get the role:', color=0x00ff00)
    
    for emoji, role_name in emoji_role_dict.items():
        embed.add_field(name=emoji, value=role_name, inline=True)
    
    message = await ctx.send(embed=embed)
    
    for emoji in emoji_role_dict.keys():
        await message.add_reaction(emoji)
@client.command(name='guess')
async def guess(ctx):
    await ctx.send("I'm thinking of a number between 1 and 100. You have 8 guesses to find it!")
    secret_number = random.randint(1, 100)
    guesses = 0
    while guesses < 8:
        guess = await client.wait_for('message', check=lambda m: m.author == ctx.author and m.content.isdigit())
        guesses += 1
        guess = int(guess.content)
        if guess == secret_number:
            await ctx.send(f"Congratulations {ctx.author.mention}, you guessed the secret number in {guesses} tries!")
            break
        elif guess < secret_number:
            await ctx.send("Your guess is too low. Try again!")
        else:
            await ctx.send("Your guess is too high. Try again!")
    else:
        await ctx.send(f"Sorry {ctx.author.mention}, you've run out of guesses. The secret number was {secret_number}.")
@client.event
async def on_raw_reaction_add(payload):
    if payload.message_id in message_ids:
        guild = client.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        if member.bot:  # ignore reactions from bots
            return

        emoji = str(payload.emoji)
        role_name = emoji_role_dict.get(emoji)
        if role_name is not None:
            role = discord.utils.get(guild.roles, name=role_name)
            if role is not None:
                await member.add_roles(role)
                             
@client.event
async def on_raw_reaction_remove(payload):
    if payload.message_id in message_ids:
        guild = client.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        if member.bot:  # ignore reactions from bots
            return

        emoji = str(payload.emoji)
        role_name = emoji_role_dict.get(emoji)
        if role_name is not None:
            role = discord.utils.get(guild.roles, name=role_name)
            if role is not None:
                await member.remove_roles(role)
@client.command()
async def edit(ctx, message_id, new_content):
    try:
        message = await ctx.channel.fetch_message(message_id)
        await message.edit(content=new_content)
        await ctx.send("Message edited successfully!")
    except discord.errors.NotFound:
        await ctx.send("Message not found.")
@client.command(name='editg', help='Edit the game list message')
async def editg(ctx):
    # Retrieve the message ID from the database
    game_message_id = 1091882503377277098
    if game_message_id is None:
        await ctx.send('Game list message not found.')
        return
    
    # Get the original message
    message = await ctx.channel.fetch_message(game_message_id)
    if message is None:
        await ctx.send('Game list message not found.')
        return
    
    # Update the message contents
    embed = discord.Embed(title='Game List', description='React to the corresponding emoji to get the role:', color=0x00ff00)
    for emoji, role_name in game_emoji_dict.items():
        embed.add_field(name=emoji, value=role_name, inline=True)
    await message.edit(embed=embed)
    
    # Add new reactions to the message
    for emoji in game_emoji_dict.keys():
        try:
            await message.add_reaction(emoji)
        except:
            pass

    await ctx.send('Game list message updated.')
@client.command(name='editr', help='Edit the rank list message')
async def editr(ctx):
    # Retrieve the message ID from the database
    rank_message_id = 1091882551498526811
    if rank_message_id is None:
        await ctx.send('Rank list message not found.')
        return
    
    # Get the original message
    message = await ctx.channel.fetch_message(rank_message_id)
    if message is None:
        await ctx.send('Rank list message not found.')
        return
    
    # Update the message contents
    embed = discord.Embed(title='Rank List', description='React to the corresponding emoji to get the role:', color=0x00ff00)
    for emoji, role_name in rank_emoji_dict.items():
        embed.add_field(name=emoji, value=role_name, inline=True)
    await message.edit(embed=embed)
    
    # Add new reactions to the message
    for emoji in rank_emoji_dict.keys():
        try:
            await message.add_reaction(emoji)
        except:
            pass

    await ctx.send('Rank list message updated.')
@client.command(name='edito', help='Edit the genral roles list message')
async def edito(ctx):
    # Retrieve the message ID from the database
    gr_message_id = 1091882440089415710
    if gr_message_id is None:
        await ctx.send('General roles list message not found.')
        return
    
    # Get the original message
    message = await ctx.channel.fetch_message(gr_message_id)
    if message is None:
        await ctx.send('General roles list message not found.')
        return
    
    # Update the message contents
    embed = discord.Embed(title='General Roles', description='React to the corresponding emoji to get the role:', color=0x00ff00)
    for emoji, role_name in general_emoji_dict.items():
        embed.add_field(name=emoji, value=role_name, inline=True)
    await message.edit(embed=embed)
    
    # Add new reactions to the message
    for emoji in general_emoji_dict.keys():
        try:
            await message.add_reaction(emoji)
        except:
            pass

    await ctx.send('General roles list message updated.')
@client.command(name='sends', help='Shows the list of available roles')
async def sends(ctx):
    embed = discord.Embed(title='Stream Announcements', description='@everyone if you want to be notified about stream announcements react to the message below:', color=0x00ff00)
    
    for emoji, role_name in stream_emoji_dict.items():
        embed.add_field(name=emoji, value=role_name, inline=True)
    
    message = await ctx.send(embed=embed)

    print(f"Use the following message ID to refer to this message: {message.id}")
    
    for emoji in stream_emoji_dict.keys():
        await message.add_reaction(emoji)

# STREAMING NOTI
@client.event 
async def check_streaming_status():
    guild = client.guilds[0]
    channel = client.get_channel(StreamChennel)
    if guild and channel:
        streamer_role = discord.utils.get(guild.roles, name=STREAMER_ROLE_NAME)
        if streamer_role:
            for member in guild.members:
                if streamer_role in member.roles and member.activity and member.activity.type == discord.StreamingActivity:
                    await channel.send(f"{streamer_role.mention} {member.display_name} is now streaming on Twitch! Check out the stream at {member.activity.url}")


@tasks.loop(seconds=cooldown_seconds)
async def clear_last_user():
    global last_user
    last_user = None

# COUNTING GAME
@client.event
async def on_message(message):
    global current_number, mistake_count, last_user, max_mistakes

    # Check if the message is sent in the counting channel and is a valid number
    if message.channel.id == counting_channel_id and message.content.isdigit():
        number = int(message.content)
        
        # Debugging prints
        # print(f"Last user: {last_user}")
        # print(f"Current user: {message.author}")
        
        if message.author == last_user:
            await message.channel.send("Please wait for someone else to send the next number.")
            return

        # Handle special numbers
        if number == 69:
            await message.add_reaction('✅')
            await message.channel.send("Nice :smirk:")
            current_number += 1
            last_user = message.author
            with open(filename, 'w') as file:
                json.dump({'current_number': current_number}, file)
        elif number == 100:
            await message.add_reaction('✅')
            await message.channel.send("hunnid hunnid")
            current_number += 1
            last_user = message.author
            with open(filename, 'w') as file:
                json.dump({'current_number': current_number}, file)
        elif number == 420:
            await message.add_reaction('✅')
            await message.channel.send("I love you, Mary Jane.")
            current_number += 1
            last_user = message.author
            with open(filename, 'w') as file:
                json.dump({'current_number': current_number}, file)
        else:
            # Check if the number is correct
            if number == current_number:
                await message.add_reaction('✅')  # Add check mark reaction
                current_number += 1
                mistake_count = 0  # Reset mistake count on correct number
                last_user = message.author
                with open(filename, 'w') as file:
                    json.dump({'current_number': current_number}, file)
            else:
                # Handle mistakes
                if current_number >= 100 and number > current_number + 5:
                    if mistake_count < max_mistakes:
                        await message.channel.send(f"Oops! {message.author.mention}, that's too far ahead. Try again. "
                                                   f"You have {max_mistakes - mistake_count} tries left.")
                        mistake_count += 1
                    else:
                        await message.channel.send("No way you just did that, try again!")
                        mistake_count = 0  # Reset mistake count after reaching the limit
                        current_number = 1
                        last_user = None
                        with open(filename, 'w') as file:
                            json.dump({'current_number': current_number}, file)
                else:
                    await message.channel.send(f"Oops! {message.author.mention} ruined it. The correct number is {current_number}.")
                    mistake_count = max_mistakes
                    #if mistake_count >= 3:  # Give 3 tries only
                        #await message.channel.send("No way you just did that, try again!")
                        #mistake_count = 0  # Reset mistake count after reaching the limit
                    current_number = 1
                    last_user = None
                    with open(filename, 'w') as file:
                        json.dump({'current_number': current_number}, file)

    await client.process_commands(message)

@client.command(name='clear', help='Clear a specified number of messages. Usage: !clear <amount>')
async def clear(ctx, amount: int):
    # Check if the command was invoked in a guild (server) and if the user has the manage_messages permission
    if ctx.guild and ctx.author.guild_permissions.manage_messages:
        # Purge (delete) the specified number of messages
        deleted = await ctx.channel.purge(limit=amount + 1)  # The +1 is to also delete the command message
        await ctx.send(f"Deleted {len(deleted)} messages.")
    else:
        await ctx.send("You don't have the manage_messages permission to use this command.")   

#custom_emojis_by_server = {}

# LISTING SERVERS
@client.command()   
async def listservers(ctx):
    servers = [guild.name for guild in client.guilds]
    await ctx.send(f"Currently in servers: {', '.join(servers)}")

# SETTING STATUS
@client.command(name='ss', help='Change the bot\'s status. Usage: !ss <status>')
async def set_status(ctx, *, status: str):
    emojied = ""
    if "<:" in status :
        emoji = status.split("<")
        emojied = emoji[1].split(">")[0]
        emojied = emojied.split(":")[2]
 
    await client.change_presence(activity=discord.CustomActivity(name=f"{status}", emoji="<a:pestoChatting:1156376824461406308>"))
    await ctx.send(f'Bot status updated to: {status}')

custom_emojis_by_server = []
# EVENT TO WRITE/READ EMOJI NAMES FROM JSON
@client.event
async def on_guild_emojis_update(guild, before, after):
    # Update the custom emojis for the server when they change
    custom_emojis_by_server[guild.id] = [emoji.name for emoji in after]
# Load custom emojis from the JSON file
def load_custom_emojis():
    try:
        with open(emoji_file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
# Save custom emojis to the JSON file
def save_custom_emojis(custom_emojis):
    with open(emoji_file_path, 'w') as file:
        json.dump(custom_emojis, file)

# COMMAND TO UPDATE EMOJI JSON
@client.command(name='upe', help='Update custom emojis in the JSON file.')
async def update_custom_emojis(ctx):
    # Fetch the custom emojis in the server
    custom_emojis = {emoji.name: emoji.id for emoji in ctx.guild.emojis}

    # Load existing custom emojis
    existing_custom_emojis = load_custom_emojis()

    # Update the custom emojis dictionary
    existing_custom_emojis[ctx.guild.id] = custom_emojis

    # Save the updated custom emojis to the JSON file
    save_custom_emojis(existing_custom_emojis)

    await ctx.send('Custom emojis updated and saved to the JSON file.')

@client.command(name='boosters', help='Show the names of server boosters.')
async def show_boosters(ctx):
    guild = ctx.guild
    boosters = guild.premium_subscribers

    if boosters:
        booster_names = ' \n'.join([booster.mention for booster in boosters])
        await ctx.send(f"These awesome people have boosted the server :) \n{booster_names} \nThank you so much! :pray:")
    else:
        await ctx.send("There are no server boosters in this server.")

async def on_ready():
    print('Bot is connected to Discord!')
    print(f'Bot is connected to the guild: {client.guilds[0].name}')

client.run('MTA5MDk5ODcxMzkwNTg0NDMwNA.G72Zsv.V1Vh-PMeyLzYn9XKuZUVdCGfOG4PDXTgUWS5pA')
