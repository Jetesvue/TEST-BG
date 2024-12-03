import discord
from discord.ext import commands, tasks
import os
import random
import event
import youtube_dl
import asyncio
from discord.utils import get
import datetime
import time
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
status = ["!info"]


@bot.event
async def on_ready():
    print("Bot is ready")
    # Schedule the changeStatus coroutine to run
    bot.loop.create_task(changeStatus())


@bot.command()
async def start(ctx, secondes=10):
    changeStatus.change_interval(seconds=secondes)


tasks.loop(seconds=10)


async def changeStatus():
    game = discord.Game(random.choice(status))
    await bot.change_presence(status=discord.Status.dnd, activity=game)


# ... rest of your code ...

musics = {}
ytdl = youtube_dl.YoutubeDL()


class Video:

    def __init__(self, link):
        video = ytdl.extract_info(link, download=False)
        video_format = video["formats"][0]
        self.url = video["webpage_url"]
        self.stream_url = video_format["url"]


@bot.command()
async def leave(ctx):
    client = ctx.guild.voice_client
    await client.disconnect()
    musics[ctx.guild] = []


@bot.command()
async def resume(ctx):
    client = ctx.guild.voice_client
    if client.is_paused():
        client.resume()


@bot.command()
async def pause(ctx):
    client = ctx.guild.voice_client
    if not client.is_paused():
        client.pause()


@bot.command()
async def skip(ctx):
    client = ctx.guild.voice_client
    client.stop()


def play_song(client, queue, song):
    source = discord.PCMVolumeTransformer(
        discord.FFmpegPCMAudio(
            song.stream_url,
            before_options=
            "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"))

    def next(_):
        if len(queue) > 0:
            new_song = queue[0]
            del queue[0]
            play_song(client, queue, new_song)
        else:
            asyncio.run_coroutine_threadsafe(client.disconnect(), bot.loop)

    client.play(source, after=next)


@bot.command()
async def play(ctx, url):
    print("play")
    client = ctx.guild.voice_client

    if client and client.channel:
        video = Video(url)
        musics[ctx.guild].append(video)
    else:
        channel = ctx.author.voice.channel
        video = Video(url)
        musics[ctx.guild] = []
        client = await channel.connect()
        await ctx.send(f"Je lance : {video.url}")
        play_song(client, musics[ctx.guild], video)


def isOwner(ctx):
    return ctx.message.author.id == 891455040131309578


drole = [
    "L'eau mouille ",
    "Le feu brule ",
    "1 + 1 = 2",
    "La terre est ronde",
    "Le soleil brille",
    "La lune est lumineuse",
    "Le vent souffle",
    "Les nuages grandissent",
]


async def createMutedRole(ctx):
    mutedRole = await ctx.guild.create_role(
        name="Muted",
        permissions=discord.Permissions(send_messages=False, speak=False),
        reason="Creation du role Muted pour mute des gens")
    for channel in ctx.guild.channels:
        await channel.set_permissions(mutedRole,
                                      send_messages=False,
                                      speak=False)
        return mutedRole


async def getMutedRole(ctx):  # Corrected: added ctx as argument
    roles = ctx.guild.roles
    for role in roles:
        if role.name == "Muted":
            return role

    return await createMutedRole(ctx
                                 )  # Corrected: passing ctx to createMutedRole


@bot.command()
@commands.check(isOwner)
async def mute(ctx, member: discord.Member, *, reason=None):
    mutedRole = await getMutedRole(ctx)
    await member.add_roles(mutedRole, reason=reason)
    await ctx.send(f"{member.mention} a été mute !")

    async def private(ctx):
        await ctx.send("Cette commande est réservée aux modérateurs !")


@bot.command()
@commands.check(isOwner)
async def unmute(ctx, member: discord.Member, *, reason=None):
    mutedRole = await getMutedRole(ctx)
    await member.remove_roles(mutedRole, reason=reason)
    await ctx.send(f"{member.mention} a été unmute !")

    async def private(ctx):
        await ctx.send("Cette commande est réservée aux modérateurs !")


@bot.command()
@commands.check(isOwner)
async def ban(ctx, user: discord.User, *, reason="None"):
    print(reason)
    reason = " ".join(reason)
    await ctx.guild.ban(user, reason=reason)
    embed = discord.Embed(title="__Un membre vient d'être banni__ !",
                          description="||Un modérateur a frappé||",
                          url="https://twitch.tv/farmautaokk",
                          color=0xff6767)
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)
    embed.set_thumbnail(
        url="https://discordemoji.com/assets/emoji/BanneHammer.png")
    embed.add_field(name="Membre", value=user.name, inline=True)
    embed.add_field(name="Raison", value=reason, inline=True)
    embed.add_field(name="Modérateur", value=ctx.author.name, inline=True)
    embed.set_footer(text=random.choice(drole))

    await ctx.send(embed=embed)

    async def private(ctx):
        await ctx.send("Cette commande est réservée aux modérateurs !")


@bot.command()
async def bonjour(ctx):
    await ctx.send(f"Bonjour {ctx.author_name} !")


@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong !")


@bot.command()
@commands.check(isOwner)
async def purge(ctx, amount=99):
    await ctx.channel.purge(limit=amount)

    async def private(ctx):
        await ctx.send("Cette commande est réservée aux modérateurs !")


@bot.command()
async def roll(ctx):
    await ctx.send(
        random.choice([
            1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
            20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36,
            37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53,
            54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70,
            71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87,
            88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100
        ]))


@bot.command()
async def info(ctx):
    await ctx.send(f"""# Voici la liste des commandes disponibles
  
  `!ping` : ||Pong||
  `!bonjour` : ||Bonjour||
  `!info` : ||Affiche la liste des commandes||
  `!roll` : ||Lance un numéro aléatoire entre 1 et 100||
  `!pub`: ||Affiche les liens de nos réseaux sociaux||
  `!message` : ||Envoie un message privé à un utilisateur||
  
  # Voici la liste des commandes disponibles pour les modérateurs
  
  `!mute` : ||Mute un membre||
  `!unmute` : ||Unmute un membre||
  `!ban` : ||Ban un membre||
  `!unban` : ||Unban un membre||
  `!purge` : ||Supprime un ou des messages du salon||
  `!say` : ||Fait parler le bot||""")


@bot.command()
@commands.check(isOwner)
async def private(ctx):
    await ctx.send("Cette commande est réservée aux modérateurs !")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(
            "Mmmmmmh, j'ai bien l'impression que cette commande n'existe pas :/"
        )

    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Il manque un argument.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send(
            "Vous n'avez pas les permissions pour faire cette commande.")
    elif isinstance(error, commands.CheckFailure):
        await ctx.send("Oups vous ne pouvez utilisez cette commande.")
    if isinstance(error.original, discord.Forbidden):
        await ctx.send(
            "Oups, je n'ai pas les permissions nécéssaires pour faire cette commmande"
        )


def good_channel(ctx):
    return ctx.message.channel.id == 724977575696400435


@bot.command()
async def coucou(ctx, nombre: int):
    for i in range(nombre):
        await ctx.send("coucou")


@coucou.error
async def coucou_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("La commande coucou prend en parametre un nombre.")
        await ctx.send("Veuillez réessayer.")


@bot.command()
@commands.has_permissions(manage_messages=True)
@commands.check(good_channel)
async def clear(ctx, nombre: int):
    messages = await ctx.channel.history(limit=nombre + 1).flatten()
    for message in messages:
        await message.delete()


@bot.command()
async def pub(ctx):
    embed = discord.Embed(title="Merci de soutenir notre bot !",
                          description="https://discord.gg/B6YYxKaPxb",
                          color=0xFFFFFF)
    await ctx.send(embed=embed)


@bot.command()
async def message(user: discord.User, *, message=None):
    message = "Bonjour, je suis un bot discord et je suis là pour vous aider !"
    embed = discord.Embed(title=message)
    await user.send(embed=embed)


@bot.command()
@commands.check(isOwner)
async def say(ctx, *, arg):
    await ctx.send(arg)

    async def private(ctx):
        await ctx.send("Cette commande est réservée aux modérateurs !")


token = os.environ['TOKEN_BOT_DISCORD']
bot.run(token)
