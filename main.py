import os
import discord
import keep_alive
from discord_slash import SlashCommand
from discord_slash.utils import manage_commands

client = discord.Client()
slash = SlashCommand(client, sync_commands=True)

content = 945812274273189928
suggestions = 696059084167708672
bugs  = 747795724758024304
admin = 814537333930983434
getrole = 911599531521609738
me = 198528960923959297
auth = os.environ['auth']

emoji_roles = {
    # Shove
    749399794371264523 : 911602092513321000
}

@client.event
async def on_ready():
    activity = discord.Activity( type=discord.ActivityType.listening, name='feedback')
    await client.change_presence(activity=activity)
    print('Logged in as', client.user)

@client.event
async def on_raw_reaction_add(payload):
    if payload.channel_id != getrole:
        return
    for i in range(len(emoji_roles)):
        if payload.emoji == await client.get_guild(payload.guild_id).fetch_emoji(list(emoji_roles.keys())[i]):
            await payload.member.add_roles(client.get_guild(payload.guild_id).get_role(list(emoji_roles.values())[i]))

@client.event
async def on_raw_reaction_remove(payload):
    if payload.channel_id != getrole:
        return
    p_guild = await client.fetch_guild(payload.guild_id)
    p_member = await p_guild.fetch_member(payload.user_id)
    for i in range(len(emoji_roles)):
        if payload.emoji == await client.get_guild(payload.guild_id).fetch_emoji(list(emoji_roles.keys())[i]):
            await p_member.remove_roles(p_guild.get_role(list(emoji_roles.values())[i]))

# Message handling
@client.event
async def on_message(message):
    # Don't respond to self
    if message.author.id == client.user.id: return

    # Echo myself
    if not message.guild:
        if message.author.id == me:
            await client.get_channel((int)(getFirst(message.content))).send(getRest(message.content))

    # Echo content for non-creators
    elif message.channel.id == content:
        contentrole = message.guild.get_role(946692883090645014)
        if contentrole in message.author.roles: return
        await message.delete()
        await message.channel.send(message.content)

    # Suggestions
    elif message.channel.id == suggestions:
        await message.delete()
        embed = discord.Embed(title=str(getFirst(message.content)).replace('-', ' ').replace('_', ' ').capitalize(), description=getRest(message.content).capitalize())
        embed.set_author(
            name=message.author.display_name,
            icon_url=message.author.avatar_url
        )
        files = []
        for x in message.attachments:
            files.append(await x.to_file())
        sent = await message.channel.send(embed=embed,files=files)
        upvote = await message.guild.fetch_emoji(843806496869187584)
        await sent.add_reaction(upvote)

    # Bugs
    elif message.channel.id == bugs:
        await message.delete()
        try:
            urgency = int(getFirst(getRest(message.content)))
        except:
            urgency = 0
        description = getRest(getRest(message.content))
        if urgency == 3:
            colour=16734296
        elif urgency == 2:
            colour=16773720
        elif urgency == 1:
            colour=8912728
        else:
            colour=2105893
            description = getRest(message.content)
        embed = discord.Embed(title=getFirst(message.content).replace('-', ' ').replace('_', ' ').capitalize(), description=description.capitalize(), color=colour)
        embed.set_author(
            name=message.author.display_name,
            icon_url=message.author.avatar_url
        )
        files = []
        for x in message.attachments:
            files.append(await x.to_file())
        await message.channel.send(embed=embed,files=files)

# Commands

# Info
info = {}
# Choices
info['choices'] = [manage_commands.create_choice(
    value = 'general',
    name = 'Grumpy Crumpet'
),
manage_commands.create_choice(
    value = 'grandma',
    name = 'Grandma\'s footsteps'),
manage_commands.create_choice(
    value = 'selfish',
    name = 'Selfish'
)]
# Options
info['options'] = [manage_commands.create_option(
        name = "topic",
        description = "What do you want to know about?",
        required = True,
        option_type = 3,
        choices = info['choices']
    )
]
# Responses
info['responses'] = {
    'general' : 'Grumpy Crumpet is an indie game dev company ran by "eel eye jar". He is developing games with a unique monochrome drawing style. <a:jumpet:820357582237597696>',
    'grandma' : 'Grandma\'s Footsteps is a *very* difficult singleplayer rage game. Don\'t play this... <#768415012812750848> <:shotgun:793272454399131648>',
    'selfish' : 'Selfish is a game about fishing, teamwork and betrayal. <#971803677901848666> <:selfish:803612012579782664>'
}
# Setup
@slash.slash(
    name='info', description='Information about a Grumpy Crumpet game', guild_ids=[692806782887788606], options=info['options']
)
async def _info(ctx, topic: str):
    if topic == 'general':
        await ctx.send(info['responses']['general'])
    elif topic == 'grandma':
        await ctx.send(info['responses']['grandma'])
    elif topic == 'selfish':
        await ctx.send(info['responses']['selfish'])

# Functions
# Get the first word of a string
def getFirst(string):
    temp = ''
    for ele in string: 
        if ele == ' ':
            if temp == '':
                return ' '
            return temp
        else: 
            temp += ele

# Get a string without it's first word
def getRest(string):
    temp = '' 
    flag = 1
    for ele in string: 
        if ele == ' ' and flag: 
            temp = '' 
            flag = 0
        else: 
            temp += ele 
    return temp

# Keep alive
keep_alive.keep_alive()

# Run
client.run(auth)