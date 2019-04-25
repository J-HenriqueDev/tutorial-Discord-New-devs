# -*- coding: utf-8 -*-
import discord
import asyncio
import random
import psutil
from time import sleep
import time, datetime
import requests
import io
import json
from googletrans import Translator
from setup import secrets
import sys
import re

# Declaração da instancia do client como bot
client = discord.Client()
# Variaveis uteis
prefixo = secrets.BOT_PREFIX
cor_padrao = secrets.BOT_COR_PADRAO
staff = secrets.STAFF


@client.event
async def on_ready():
    """ Evento de ready do bot , vai printar algumas informaçoes e alterar o status do bot"""
    print("=================================")
    print(f"Nome: {client.user.name}")
    print(f"ID: {client.user.id}")
    print(f"On line em : {str(len(client.guilds))} Servidores")
    print(f'Com {str(len(set(client.get_all_members())))} usuarios')
    print(f"Bot Versão: {secrets.BOT_VERSAO}")
    print("=================================")
    await client.change_presence(status=discord.Status, activity=discord.Game("Vagner tutorial"))


@client.event
async def on_member_join(member):
    """ Evento que dispara ao membro entrou em um servidor, vai printar o nome do membro e de qual servidor ele entrou"""
    print(f"o membro {member.name} entrou no servidor {member.guild.name}")


@client.event
async def on_member_remove(member):
    """ Evento que dispara ao membro ser removido de um servidor, vai printar o nome do membro e de qual servidor ele saiu"""
    print(f"o membro {member.name} saiu do servidor {member.guild.name}")


@client.event
async def on_guild_join(guild):
    """ Evento que dispara quando bot é adicionado em um servidor, vai printar o nome do servidor"""
    print(f"Entrei no sevidor {guild.name}")


@client.event
async def on_guild_remove(guild):
    """ Evento que dispara quando bot é removido em um servidor, vai printar o nome do servidor"""
    print(f"Removido do sevidor {guild.name}")


@client.event
async def on_error(event, *args, **kwargs):
    """Evento de erro do bot"""
    print(f"Erro no evento: {event}\nErro: {sys.exc_info()}")


@client.event
async def on_message(message):
    """Evento de messagem recebida do bot. Aqui vai todos comando"""

    # Para iginorar bots
    if message.author.bot:
        return

    # Canal de votaçaõ
    canal_de_votacao = client.get_channel(564892379967127573)
    if message.channel.id == canal_de_votacao.id:
        await message.add_reaction("👍")
        await message.add_reaction("👎")


    # Ao mencionar o bot enviar uma messagem
    elif message.content.lower().startswith(f"<@!{client.user.id}>") or message.content.lower().startswith(
            f"<@{client.user.id}>"):
        await message.channel.send(f"use `{prefixo}ajuda` para ver meus comandos.")

    # Comando de ajuda
    elif message.content.lower().startswith(prefixo + 'ajuda'):
        embedAjuda = discord.Embed(color=cor_padrao, description=f"Prefixo `{prefixo}`\nCommandos `29`")
        embedAjuda.add_field(name='🔐 Moderação (06)', value='`servbans,ban,jogando,apagar,mute,unmute`')
        embedAjuda.add_field(name='⛏ Utilidades (06)', value='`convite,reportarbug,hora,votar,aviso,traduzir`')
        embedAjuda.add_field(name='🔍 Informaçao (10)', value='`botinfo,serverinfo,userinfo,emojis,noticia,cargos,avatar,ping,canalinfo,status`')
        embedAjuda.add_field(name='🎊 Diversão (07)',value='`loteria,diz,moeda,virus,dado,gatogif,gato`')
        embedAjuda.set_footer(
            text="Comando usado por {} as {} Hrs".format(message.author, datetime.datetime.now().hour),
            icon_url=message.author.avatar_url)
        await message.channel.send(embed=embedAjuda)



    # ======MODERAÇÂO ======

    # COMANDO 1
    elif message.content.lower().startswith(prefixo + "servbans"):
        if not message.author.guild_permissions.ban_members:
            await message.channel.send("⛔ **Permissão insuficiente.**")
            return
        try:
            servidor = client.get_guild(message.guild.id)

            banlist = await servidor.bans()
            if len(banlist) == 0:
                await message.channel.send("⚠ Esse sever não possui usuarios banidos")
            else:
                text = "\n".join([f"{x.user} ({x.user.id})" for x in banlist])
                bansembed = discord.Embed(title='`Banimentos do servidor` {}'.format(message.guild.name),
                                          color=cor_padrao, description=text)
                await message.channel.send(embed=bansembed)
        except discord.errors.Forbidden:
            await message.channel.send('⚠ não possuo permissões para ver os banimentos desse servidor')

        except Exception as e:
            await message.channel.send('Ocorreu um erro : `{}`'.format(e))


    # COMANDO 2
    elif message.content.lower().startswith(prefixo + 'ban'):
        if not message.author.guild_permissions.ban_members:
            await message.channel.send("⛔ **Permissão insuficiente.**")
            return
        try:
            await message.guild.ban(message.mentions[0])
            await message.channel.send(f"`{message.author}` Baniu `{message.mentions[0]}` com sucesso.")
        except IndexError:
            await message.channel.send(f"**exemplo**: `{prefixo}ban [menção do membro]`")


    # COMANDO 3
    elif message.content.startswith(prefixo + "jogando"):
        novo_status = message.content.replace(f"{prefixo}jogando", "")
        if message.author.id in staff:
            await client.change_presence(status=discord.Status, activity=discord.Game(novo_status))
            await message.channel.send("**Status bot alterado para:** `{}`".format(novo_status))
        else:
            await message.channel.send("⛔ **Somente meu adiministradores podem usar esse comando.**", delete_after=20)


    # COMANDO 4
    elif message.content.lower().startswith(prefixo + 'apagar'):
        if not message.author.guild_permissions.ban_members:
            await message.channel.send("⛔ **Permissão insuficiente.**")
            return
        limite = int(message.content.replace(f"{prefixo}apagar", ""))
        deletados = await message.channel.purge(limit=limite)
        await message.channel.send(f"**foram deletadas** `{len(deletados)}`  **messagens por** `{message.author}`",
                                   delete_after=20)


    # COMANDO 5
    elif message.content.lower().startswith(prefixo + "mute"):
        if not message.author.guild_permissions.ban_members:
            await message.channel.send("⛔ **Permissão insuficiente.**")
            return

        cargo = discord.utils.get(message.guild.roles, name='Mutado')

        if cargo == None:
            await message.channel.send("⛔ **O servidor não possui o cargo:** `Mutado`")
            return
        try:
            membro = message.mentions[0]
            await membro.add_roles(cargo, reason="Usuario mutado")
            await message.channel.send(f"**O membro `{membro}` foi mutado por `{message.author}`**")
        except IndexError:
            await message.channel.send(f"**exemplo**: `{prefixo}mute [menção do membro]`")



    # COMANDO 6
    elif message.content.lower().startswith(prefixo + "unmute"):
        if not message.author.guild_permissions.ban_members:
            await message.channel.send("⛔ **Permissão insuficiente.**")
            return
        cargo = discord.utils.get(message.guild.roles, name='Mutado')

        if cargo == None:
            await message.channel.send("⛔ **O servidor não possui o cargo:** `Mutado`")
            return
        try:
            membro = message.mentions[0]
            await membro.remove_roles(cargo, reason="Usuario desmutado")
            await message.channel.send(f"**O membro `{membro}` foi desmutado por `{message.author}`**")
        except IndexError:
            await message.channel.send(f"**exemplo**: `{prefixo}mute [menção do membro]`")

    # ======UTILIDADES ======

    # COMANDO 1
    elif message.content.startswith(prefixo + "convite"):

        try:
            invite = await message.channel.create_invite(max_uses=2, temporary=True, xkcd=True)
            await message.channel.send(f"**Convite criado**\n{invite}")

        except Exception as e:
            print(e)
            await message.channel.send("**Falha ao criar o convite**")

    # COMANDO 2
    elif message.content.lower().startswith(prefixo + 'reportarbug'):
        await message.delete()
        bug = message.content.replace(f"{prefixo}reportarbug", "")
        canal_de_bugs = client.get_channel(557194044548055040)
        if len(bug) > 1:
            await canal_de_bugs.send(f"Bug reportado por {message.author} \n BUG:` {bug}`")
            await message.channel.send("✅ **Bug reportado.**", delete_after=30)
        else:
            await message.channel.send("❗️**Insira qual bug foi encontrado.**", delete_after=30)



    # COMANDO 3
    elif message.content.startswith(prefixo + "hora"):
        dt = datetime.datetime.now()
        msg = "`📅 {}/{}/{}` `⏰ {}:{}:{}`".format(dt.day, dt.month, dt.year, dt.hour, dt.minute, dt.second)
        await message.channel.send(msg)


    # COMANDO 4
    elif message.content.lower().startswith(prefixo + 'votar'):
        await message.delete()
        try:
            titulo = message.content.replace(f"{prefixo}votar", "")
            embedvotar = discord.Embed(
                title="**VOTAÇÃO**"
                , color=cor_padrao
            )
            embedvotar.set_thumbnail(url=message.author.avatar_url)
            embedvotar.add_field(name='`📝 Votação iniciada por`', value=message.author.mention, inline=False)
            embedvotar.add_field(name='`🖋 Titulo`', value="{}".format(titulo), inline=False)

            reagir = await message.channel.send(embed=embedvotar)
            await reagir.add_reaction('✔')
            await reagir.add_reaction('❌')
        except discord.errors.HTTPException:
            await message.channel.send(f"**Exemple**`{prefixo}votar [Titulo]`", delete_after=20)


    # COMANDO 5
    elif message.content.lower().startswith(prefixo + "aviso"):
        await message.delete()
        user = message.author
        aviso = message.content.replace(f"{prefixo}aviso", "")
        if not aviso:
            await message.channel.send(f"**Exemplo**`{prefixo}aviso [Texto]`")
            return
        embed = discord.Embed(
            title=" :loudspeaker: AVISO :loudspeaker:",
            description="{}".format(aviso),
            color=cor_padrao
        )
        embed.set_footer(
            text="Enviado por: " + user.name,
            icon_url=user.avatar_url
        )

        await message.channel.send("@here", embed=embed)



    # COMANDO 6
    elif message.content.lower().startswith(prefixo + "traduzir"):
        await message.channel.send(
            '**Selecione uma opçao para traduzir** \n `1`  **Para o ingles** \n `2` **Passando linguagem de saida**')

        def checar(msg):
            return message.author == msg.author and message.channel == msg.channel

        selecao = await client.wait_for('message', timeout=120, check=checar)
        translator = Translator()
        msg = 'Ocorreu um error'
        await message.channel.send('**insira o texto**')
        traduzir = await client.wait_for('message', timeout=120, check=checar)

        try:
            if selecao.content == '1':
                resultado = translator.translate(traduzir.content)
            elif selecao.content == '2':
                await message.channel.send('Coloque a linguagem para traduzir')
                lang_traduzir = await client.wait_for("message", timeout=120, check=checar)
                resultado = translator.translate(traduzir.content, lang_traduzir.content)
            else:
                await message.channel.send('❗**Seleção cancelada**')
                return
        except:
            await message.channel.send('❗ **Erro ao buscar linguagem**')
            return
        if (resultado):
            msg = f'**Resultado:** `{resultado.text}` '
        await message.channel.send(msg)
        return



    # ======INFORMAÇÂo ======

    # COMANDO 1
    elif message.content.lower().startswith(prefixo + 'botinfo'):
        embedbot = discord.Embed(
            title='**Info do Bot**',
            color=cor_padrao,
        )
        embedbot.add_field(name='`💮 | Nome`', value=client.user.name, inline=True)
        embedbot.add_field(name='`◼ | Id bot`', value=client.user.id, inline=True)
        embedbot.add_field(name='`💠 | Criado em`', value=client.user.created_at.strftime("%d %b %Y %H:%M"))
        embedbot.add_field(name='‍`💻 | Servidores`', value=len(client.guilds))
        embedbot.add_field(name='‍`🧐 | Emojis`', value=len(client.emojis))
        embedbot.add_field(name='`👥 | Usuarios`', value=len(list(client.get_all_members())))
        embedbot.set_footer(
            text="Comando usado por {} as {} Hrs".format(message.author, datetime.datetime.now().hour),
            icon_url=message.author.avatar_url)

        await message.channel.send(embed=embedbot)

    # COMANDO 2
    elif message.content.lower().startswith(prefixo + 'serverinfo'):
        guilda = message.guild
        created_at = f'{guilda.created_at.strftime("%d %b %Y %H:%M")}'
        embedbot = discord.Embed(title='`Server Info`', color=cor_padrao)
        embedbot.set_thumbnail(url=message.guild.icon_url)
        embedbot.add_field(name='`☣ | Nome`', value=guilda.name, inline=True)
        embedbot.add_field(name='`👑 | Dono`', value=guilda.owner)
        embedbot.add_field(name='`🕳️ | Id`', value=guilda.id)
        embedbot.add_field(name='`📅 | Criado em`', value=created_at, inline=False)
        embedbot.add_field(name='`👥 | Cargos`', value=len(guilda.roles), inline=True)
        embedbot.add_field(name='`🌐 | Região`', value=guilda.region, inline=True)
        embedbot.add_field(name='`🧐 | Emojis`', value=(len(guilda.emojis)), inline=True)
        embedbot.add_field(name='`🔇 | Canal de afk`', value=guilda.afk_channel, inline=True)
        embedbot.add_field(name='🔐 ﾠ | Segurança', value=guilda.verification_level, inline=True)
        embedbot.add_field(name='`👨‍👦‍👦ﾠ   | Membros`', value=len(guilda.members), inline=True)
        embedbot.add_field(name='`🤖 | Bots`', value=str(len(list(member for member in guilda.members if member.bot))))
        embedbot.add_field(name='🌀 | Cargo padrão', value=guilda.default_role, inline=True)
        embedbot.add_field(name='📷 | Icon server', value=f"[DOWNLOAD]({guilda.icon_url_as(format='png')})", inline=True)
        embedbot.set_footer(
            text="Comando usado por {} as {} Hrs".format(message.author, datetime.datetime.now().hour),
            icon_url=message.author.avatar_url)
        await message.channel.send(embed=embedbot)


    # COMANDO 3
    elif message.content.lower().startswith(prefixo+'userinfo'):

          try:
            membro = message.mentions[0]
          except:
            membro = message.author

          embedinfo = discord.Embed(
              title=f'informações sobre o membro {membro.display_name}',
              color=cor_padrao,
          )
          embedinfo.set_thumbnail(url=membro.avatar_url)
          embedinfo.add_field(name='`☣ | Usuário`', value=membro.name)
          embedinfo.add_field(name='`🤬  | Apelido`', value=membro.nick)
          embedinfo.add_field(name='`🕳️ | Id`', value=membro.id)
          embedinfo.add_field(name='`📅 | Desde de`', value=membro.created_at.strftime("%d %b %Y %H:%M"))
          embedinfo.add_field(name='`🗓️ | Entrou em`', value=membro.joined_at.strftime("%d %b %Y %H:%M"))
          embedinfo.add_field(name='`🎮 | Jogando`', value=membro.activity.name)
          embedinfo.add_field(name='`💎 | Cargos`',value=len(([role.name for role in membro.roles if role.name != "@everyone"])))
          embedinfo.set_footer(
           text="Comando usado por {} as {} Hrs".format(message.author, datetime.datetime.now().hour),
           icon_url=message.author.avatar_url)
          await message.channel.send(embed=embedinfo)

    # COMANDO 4
    elif message.content.lower().startswith(prefixo+"emojis"):
        msg = ' '.join([str(x) for x in message.guild.emojis])
        embedmo = discord.Embed(title=f"Emojis do Servidor `{message.guild.name} ({len(message.guild.emojis)}) emojis`", description=msg, color=cor_padrao)
        embedmo.set_thumbnail(url=f"{message.guild.icon_url}")
        embedmo.set_footer(text="Comando usado por {} as {} Hrs".format(message.author, datetime.datetime.now().hour),
                           icon_url=message.author.avatar_url)
        await message.channel.send(embed=embedmo)

    # COMANDO 5
    elif message.content.lower().startswith(prefixo+'noticia'):

        reqnews = requests.get(
            'https://newsapi.org/v2/top-headlines?sources=globo&apiKey=41e3884b04e24c70a3ae95b99e675a20')
        lernews = json.loads(reqnews.text)
        authornews = (str(lernews['articles'][0]['author']))
        titulonews = (str(lernews['articles'][0]['title']))
        descriptionnews = (str(lernews['articles'][0]['description']))
        urlnews = (str(lernews['articles'][0]['url']))
        datanews = (str(lernews['articles'][0]['publishedAt']))
        imgnews = (str(lernews['articles'][0]['urlToImage']))
        embednews = discord.Embed(color=cor_padrao)
        embednews.add_field(name='Author:', value="{}".format(authornews))
        embednews.add_field(name='Titulo:', value="{}".format(titulonews))
        embednews.add_field(name='Descrição:', value="{}".format(descriptionnews))
        embednews.add_field(name='Url da noticia:', value="{}".format(urlnews))
        embednews.set_footer(text='Data da noticia: ' + datanews)
        embednews.set_thumbnail(url=imgnews)
        await message.channel.send(embed=embednews)


    # COMANDO 6
    elif message.content.lower().startswith(prefixo+"cargos"):
        cargos = [role.name for role in message.guild.roles if role.name != "@everyone"]
        role = discord.Embed(title='Cargos do servidor {}'.format(message.guild.name),
                             description='Total [{}] Cargos'.format(len(message.guild.roles)), color=0x1CF9FF)
        role.set_thumbnail(url=message.guild.icon_url)
        role.add_field(name="`Lista`", value='{}'.format(cargos).replace("'", " ").replace("[", " ").replace("]", " "))
        role.set_footer(
            text="Comando usado por {} as {} Hrs".format(message.author, datetime.datetime.now().hour),
            icon_url=message.author.avatar_url)
        await message.channel.send(embed=role)

    # COMANDO 7
    elif message.content.lower().startswith(prefixo+'avatar'):
           try:
            member = message.mentions[0]
           except:
            member = message.author

           embed = discord.Embed(
                title=f'📷 avatar do {member.name}',
                color=member.color,
                description=f"[DOWNLOAD]({member.avatar_url})")
           embed.set_image(url=member.avatar_url)
           embed.set_footer(text=f"{client.user.name}", icon_url=client.user.avatar_url)
           await message.channel.send(embed=embed)


    # COMANDO 8
    elif message.content.lower().startswith(prefixo+'ping'):
        await message.channel.send(f"🏓 **pong** `{round(client.latency,2)} ms`")

    # COMANDO 9
    elif message.content.lower().startswith(prefixo+'canalinfo'):
        channel = message.channel
        embed = discord.Embed(color=cor_padrao,
                              description=channel.mention)
        embed.add_field(name="Nome", value=message.channel.name, inline=True)
        embed.add_field(name="Server", value=message.channel.guild.name, inline=True)
        embed.add_field(name="ID", value=channel.id)
        embed.add_field(name="Posição", value=channel.position + 1)
        embed.add_field(name="Criado em", value=message.channel.created_at.strftime("%d %b %Y %H:%M"))
        embed.set_footer(
            text="Comando usado por {} as {} Hrs".format(message.author, datetime.datetime.now().hour),
            icon_url=message.author.avatar_url)
        await message.channel.send(embed=embed)



    # COMANDO 10
    elif message.content.startswith(prefixo+'status'):

        ram = psutil.virtual_memory().percent
        embed = discord.Embed(title='Bot Status', color=cor_padrao,description='`DISCORD STATUS`')
        embed.add_field(name="🌐 Servidores", value="\n```javascript\n{} \n```".format((len(client.guilds))))
        embed.add_field(name="👥 Usuarios",value="\n```javascript\n{} \n```".format(len(set(client.get_all_members()))))
        embed.add_field(name="💬 Canais", value="\n```javascript\n{} \n```".format(len(set(client.get_all_channels()))))
        embed.add_field(name='ﾠ', value='`CPU STATUS`', inline=False)
        embed.add_field(name="💾 Ram used", value="\n```javascript\n{} mb \n```".format(ram))
        embed.add_field(name="🖥 Cpu used",value="\n```javascript\n{} % \n```".format(str(psutil.cpu_percent(interval=1))))
        embed.set_footer(text="Comando usado por {} as {} Hrs".format(message.author, datetime.datetime.now().hour),
                         icon_url=message.author.avatar_url)
        await message.channel.send(embed=embed)



    # ======DIVERSÂO ======
    # COMANDO 1
    elif message.content.lower().startswith(prefixo+'loteria'):

        try:
            numero = int(message.content.strip(prefixo+'loteria').strip())
            float(numero)
            numero += 1
        except ValueError:
            await message.channel.send('😝 **Escolha um numero e tente a sorte** ')
        else:
            number = random.randint(1, 100)
            rol = await message.channel.send('🎰 Rodando...')
            sleep(2)
            if number == int(message.content.strip(prefixo+'loteria').strip()):
                await rol.edit(content=f'**Ganhou!** o numero foi `{str(number)}` ')
            else:
                await rol.edit(content=f'**Perdeu!**. O numero foi `{str(number)}`')

    # COMANDO 2
    elif message.content.lower().startswith(prefixo+'diz'):
        await message.delete()
        msg = message.content.replace(f"{prefixo}diz", "").replace("@everyone","💣").replace("@here","💣")
        if not msg:
            await message.channel.send(f"**Exemplo:** `{prefixo}diz [Texto]`")
            return
        else:
           await message.channel.send(msg)


    # COMANDO 3
    elif message.content.startswith(prefixo+'moeda'):
        # await client.delete_message(message)
        choice = random.randint(1, 2)
        if choice == 1:
            await message.add_reaction('👑')
        if choice == 2:
            await message.add_reaction('😃')

    # COMANDO 4
    elif message.content.lower().startswith(prefixo+'virus'):
        await message.delete()
        try:
          user = message.mentions[0]
        except:
            user = message.author

        incio = await message.channel.send("💉 **iniciando**...")
        await asyncio.sleep(3.0)
        await incio.edit(content="[▓                         ] / -virus.bat Packing files.")
        await asyncio.sleep(0.5)
        await incio.edit(content="[▓▓                    ] - -virus.bat Packing files..")
        await asyncio.sleep(0.7)
        await incio.edit(content= "[▓▓▓            ] | -virus.bat Packing files..")
        await asyncio.sleep(1.0)
        await incio.edit(content= "[▓▓▓▓        ] / -virus.bat Packing files..")
        await asyncio.sleep(0.5)
        await incio.edit(content= "[▓▓▓▓▓    ] - -virus.bat Packing files..")
        await asyncio.sleep(0.8)
        await incio.edit(content= "[▓▓▓▓▓▓] \ -virus.bat Packing files..")
        await asyncio.sleep(4.0)
        await incio.edit(content= "[▓▓▓▓▓▓] - -virus.bat Packing files..")
        await asyncio.sleep(0.8)
        await incio.edit(content= "[▓▓▓▓▓▓] \ -virus.bat Packing files..")
        await asyncio.sleep(0.5)
        await incio.edit(content= "[▓▓▓▓▓▓] - -virus.bat Packing files..")
        await asyncio.sleep(1.2)
        await incio.edit(content= "[▓▓▓▓▓▓] / -virus.bat Packing files..")
        await asyncio.sleep(1.0)
        await incio.edit(content= "[▓▓▓▓▓▓] - -virus.bat Packing files..")
        await asyncio.sleep(0.8)
        await incio.edit(content= "[▓▓▓▓▓▓] \ -virus.bat Packing files..")
        await asyncio.sleep(0.8)
        await incio.edit(content= "instalando virus...")
        await asyncio.sleep(0.5)
        await incio.edit(content= f"🈴 ** Ok virus instalanado no pc do** `{user.name}`")
        await asyncio.sleep(1.0)
        await incio.delete()




    # COMANDO 5
    elif message.content.startswith(prefixo+"dado"):
        # await client.delete_message(message)
        choice = random.randint(1, 6)
        embeddad = discord.Embed(title='🎲 Dado', description=' Joguei o dado, o resultado foi :   {}'.format(choice),
                                 colour=cor_padrao)
        await message.channel.send(embed=embeddad)


    # COMANDO 6
    elif message.content.lower().startswith(prefixo+'gatogif'):
        # await client.delete_message(message)
        embgif = discord.Embed(
            title='Gato Gif',
            color=cor_padrao,

        )

        embgif.set_image(url=requests.get('http://thecatapi.com/api/images/get?format=src&type=gif').url)
        embgif.set_footer(
            text="Comando usado por {} as {} Hrs".format(message.author, datetime.datetime.now().hour),
            icon_url=message.author.avatar_url)
        await message.channel.send(embed=embgif)

    # COMANDO 7
    elif message.content.lower().startswith(prefixo+'gato'):

        embimg = discord.Embed(
            title='Gato',
            color=cor_padrao,

        )
        embimg.set_image(url=requests.get('http://thecatapi.com/api/images/get?format=src&type=jpg').url)
        embimg.set_footer(
            text="Comando usado por {} as {} Hrs".format(message.author, datetime.datetime.now().hour),
            icon_url=message.author.avatar_url)
        await message.channel.send(embed=embimg)



client.run(secrets.BOT_TOKEN)
