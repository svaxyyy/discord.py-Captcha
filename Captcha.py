import discord
from discord.ext import commands
from io import *
from discord.embeds import Embed
from discord.ext.commands.core import command
from discord_components import *
from discord_components import DiscordComponents, Button, Select, SelectOption, Component
from datetime import *
from discord_components import client
from captcha.image import ImageCaptcha
from random import randrange
import json




intents = discord.Intents.default()
intents.members = True


color = 0xffffff

# json


def load():
    with open("database/json/bot_config.json", "r") as file:
        return json.load(file)


data = load()

client = commands.Bot(command_prefix=data["prefix"], intents=intents)
client.launch_time = datetime.utcnow()



@client.event
async def on_ready():
    DiscordComponents(client)
    print('We have logged in as {0.user}'.format(client))





@client.command()
@commands.has_permissions(administrator=True)
async def setup_captcha(ctx):
    with open("database/json/captcha-configs.json", "r") as f:
        setupdata = json.load(f)

    if not ctx.guild.id in setupdata:
        setupdata = {}
        setupdata["verified-role-id"] = 0
        with open("database/json/captcha-configs.json", "w") as f:
            json.dump(setupdata,f)


    def mcheck(m):
        return m.author is not None and m.author == ctx.author


    embed = discord.Embed(title="Captcha System Setup", description="Please ping the Role which i will give the user. for example @verified ", color=color)
    embed.set_footer(text=ctx.guild.name, icon_url=f"{ctx.guild.icon_url}")
    embed.timestamp = datetime.utcnow()
    msg1 = await ctx.send(embed=embed)
    msg = await client.wait_for('message', check=None)
    setupdata["role-ids"] = msg.role_mentions[0].id
    await msg1.add_reaction("✅")
    with open("database/json/captcha-configs.json", "w") as f:
        json.dump(setupdata,f)

    embed = discord.Embed(title="Captcha System Setup", description="Sucessfully finished the Setup!", color=color)
    embed.set_footer(text=ctx.guild.name, icon_url=f"{ctx.guild.icon_url}")
    embed.timestamp = datetime.utcnow()
    msg1 = await ctx.send(embed=embed)
    await msg1.add_reaction("✅")
    with open("database/json/captcha-configs.json", "w") as f:
        json.dump(setupdata,f)






@client.command(aliases=["verify"])
async def captcha(ctx):
    with open("database/json/captcha-configs.json", "r") as f:
        setupdata = json.load(f)
    
    guild = client.get_guild(ctx.message.guild.id)
    member = guild.get_member(ctx.author.id)
    role = guild.get_role(setupdata["verified-role-id"])
    number = randrange(9999)
    num1=randrange(1,1999)
    num2=randrange(2000,3999)
    num3=randrange(4000, 5999)
    num4=randrange(6000,9999)
    print(number)
    image = ImageCaptcha(width = 280, height = 90)
    data = image.generate(f"{number}")
    image.write(f"{number}", 'database/captcha/captcha.png')
    file = discord.File('database/captcha/captcha.png')
    await ctx.author.send(file=file)
    embed = Embed(title="Captcha🤖", description="Please select the Code which is on the Picture!")
    msg = await ctx.author.send(embed=embed, components=[Select(placeholder="Select here!",options=[
        SelectOption(
            label=f"{num1}",
            value="1",
            description="Option 1",
            emoji="↗️"
        ),
        SelectOption(
            label=f"{num2}",
            value="2",
            description="Option 2",
            emoji="↗️"
        ),
        SelectOption(
            label=f"{num3}",
            value="3",
            description="Option 3",
            emoji="↗️"
        ),
        SelectOption(
            label=f"{num4}",
            value="4",
            description="Option 4",
            emoji="↗️"
        ),
        SelectOption(
            label=f"{number}",
            value="5",
            description="Option 5",
            emoji="↗️"
        )
        ])])



    res = await client.wait_for("select_option")

    
    label = res.component[0].label
    if label == f"{num1}":
        await res.respond(type=6)
        emb = Embed(title="Captcha🤖", description="`Captcha failed!` It seems like you have 1IQ or you are a bot!❌")
        msg1 = await res.user.send(embed=emb)
        await msg1.add_reaction("❌")
        await ctx.message.add_reaction("❌")
        await msg.edit(components=[])

    if label == f"{num2}":
        await res.respond(type=6)
        emb = Embed(title="Captcha🤖", description="`Captcha failed!` It seems like you have 1IQ or you are a bot!❌")
        msg1 = await res.user.send(embed=emb)
        await msg1.add_reaction("❌")
        await ctx.message.add_reaction("❌")
        await msg.edit(components=[])


    if label == f"{num3}":
        await res.respond(type=6)
        emb = Embed(title="Captcha🤖", description="`Captcha failed!` It seems like you have 1IQ or you are a bot!❌")
        msg1 = await res.user.send(embed=emb)
        await msg1.add_reaction("❌")
        await ctx.message.add_reaction("❌")
        await msg.edit(components=[])

    if label == f"{num4}":
        await res.respond(type=6)
        emb = Embed(title="Captcha🤖", description="`Captcha failed!` It seems like you have 1IQ or you are a bot!❌")
        msg1 = await res.user.send(embed=emb)
        await msg1.add_reaction("❌")
        await ctx.message.add_reaction("❌")
        await msg.edit(components=[])
        

    if label == f"{number}":
        await res.respond(type=6)
        emb = Embed(title="Captcha🤖", description="`Captcha Sucessfully!` You are now sucessfully verified as a human!✅")
        msg1 = await res.user.send(embed=emb)
        await msg1.add_reaction("✅")
        await msg.edit(components=[])
        await ctx.message.add_reaction("✅")
        await member.add_roles(role)










client.run(data["token"])