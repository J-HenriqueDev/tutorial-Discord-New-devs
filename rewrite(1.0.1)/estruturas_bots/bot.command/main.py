import discord
from discord.ext import commands
import os
import time
import re
import asyncio
from setup import secrets




TOKEN = secrets.BOT_TOKEN
COR_PADRAO = secrets.BOT_COR_PADRAO
PREFIXO = commands.when_mentioned_or("n!")


bot = commands.Bot(command_prefix=PREFIXO, description='Vagner Tutorial')
bot.remove_command('help')


@bot.event
async def on_ready():
    print(f'{bot.user.name} Online')
    print(f'{len(bot.guilds)} Servidores')
    print('-='*20)
    await bot.change_presence(status=discord.Status, activity=discord.Game("Vagner tutorial"))



@bot.command()
async def ban(ctx, member: discord.Member):
    if ctx.message.author.guild_permissions.ban_members:
           await member.ban(reason="Usuario banido")
           await ctx.send("{} Banido".format(member.mention))
    else:
        await ctx.send('❗**Permissão insuficiente**')

@ban.error
async def ban_error(ctx,erro):
    if isinstance(erro,commands.MissingRequiredArgument):
        await ctx.send(f"**Exemplo** `n!ban [Nome, meçao ou id do membro]`")
        return
    else:
        await ctx.send(f'❗**Falha ao banir**\n```javastript\n{erro}\n```')
        return


@bot.command()
async def kick(ctx, member: discord.Member):
    if ctx.message.author.guild_permissions.ban_members:
           await member.kick(reason="Usuario kikado")
           await ctx.send("{} Banido".format(member.mention))
    else:
        await ctx.send('❗**Permissão insuficiente**')

@kick.error
async def kick_error(ctx,erro):
    if isinstance(erro,commands.MissingRequiredArgument):
        await ctx.send(f"**Exemplo** `n!kick [Nome, meçao ou id do membro]`")
        return
    else:
        await ctx.send(f'❗**Falha ao kikar**\n```javastript\n{erro}\n```')
        return


@bot.command()
async def ping(ctx):
    await ctx.send(f"🏓 **Pong** `{round(bot.latency,2)}ms`")



bot.run(TOKEN)