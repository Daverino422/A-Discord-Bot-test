import asyncio

import discord
from discord.commands import Option
import random
import os
from dotenv import load_dotenv

activity = discord.CustomActivity(
    "Testbot by daverino22",
)
intents = discord.Intents.default()

bot = discord.Bot(
    activity=activity,
    intents=intents,
    debug_guilds=[605748920773247044]
)

def zufaellige_zeile_aus_datei(datei_pfad):
    # Öffne die Datei und lese alle Zeilen ein
    with open(datei_pfad, 'r', encoding='utf-8') as datei:
        zeilen = datei.readlines()

    # Wähle eine zufällige Zeile aus
    zufaellige_zeile = random.choice(zeilen)

    return zufaellige_zeile.strip()  # .strip() entfernt führende und nachfolgende Leerzeichen, einschließlich Zeilenumbrüche

# Beispiel für die Verwendung
datei_pfad = 'quotes.txt'  # Ersetze 'deine_datei.txt' durch den Pfad zu deiner Datei
zufaellige_zeile = zufaellige_zeile_aus_datei(datei_pfad)

@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")


@bot.slash_command(description="Curse out a user")
async def curse(ctx, user: Option(discord.Member, "The user you want to curse out")):
    await ctx.respond(f"Fuck you! {user.mention}")


@bot.slash_command(description="Let the bot send a message")
async def say(ctx,
              text: Option(str, "The message you want to say"),
              channel: Option(discord.TextChannel, "The channel you want to send the message to"),
              ):
    await channel.send(text)
    await ctx.respond(f"message sent successfully!", ephemeral=True)

@bot.slash_command(description="Get info on a user")
async def info(ctx, alter: Option(int, "Age", min_value=1, max_value=100), user: Option(discord.Member, "The user you want the info on")):
    if user is None:
        user = ctx.author
    embed = discord.Embed(
        title=f"{user.name}'s info",
        description=f"all information about{user.mention}",
        color=discord.Color.blue()
    )

    time = discord.utils.format_dt(user.created_at, "R")

    embed.add_field(name="Account Created:", value=time, inline=False)
    embed.add_field(name="ID", value=user.id)
    embed.add_field(name="Age", value=alter)

    embed.set_thumbnail(url=user.avatar.url)
    embed.set_footer(text="Bot by Daverino22")

    await ctx.respond(embed=embed)

@bot.slash_command(description="Get user profile picture")
async def profilepic(ctx, user: Option(discord.Member, "The users profile picture you want to get")):
    if user is None:
        user = ctx.author
    embed = discord.Embed(
        title=f"{user.name}'s profile picture",
    )
    embed.add_field(name="Person:", value=user)
    embed.set_thumbnail(url=user.avatar.url)

    embed.set_footer(text="Bot by Daverino22")

    await ctx.respond(embed=embed)


@bot.slash_command(description="Get me a random Drachenlord quote")
async def drachequote(ctx):
    embed = discord.Embed(
        title="Drachengame",
    )

    embed.add_field(name=f"Quote:",value=zufaellige_zeile_aus_datei('quotes.txt'))
    embed.set_thumbnail(url='https://cdn.daverino.de/media/3bexa.png')
    embed.set_footer(text="Bot by Daverino22")

    await ctx.respond(embed=embed)

load_dotenv()
bot.run(os.getenv('TOKEN'))
