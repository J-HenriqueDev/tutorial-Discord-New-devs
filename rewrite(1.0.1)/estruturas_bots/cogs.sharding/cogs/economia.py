from discord.ext import commands
from database import mongodb as db
import discord


# Lembre sempre de colocar o commnads.Cog
class economia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    # Essa é uma funcão para setar um cooldown no membro
    @commands.cooldown(1, 10800, commands.BucketType.user)
    async def rep(self, ctx, membro: discord.Member):
        """ Vamos bloquer pontos para bots """
        if membro.bot is True:
            await ctx.send(f"**Não posso adiconar pontos  de reputação para um bot!**")
            return
        # Vamos bloquear para adicionar pontos pra si propio
        if ctx.message.author.id == membro.id:
            await ctx.send(f"**Voçê não pode adicionar pontos para si mesmo!**")
            return
        rep = 1
        db.verificar(membro.id)
        db.setar_reputacao(membro.id,rep)
        atual = db.buscar(membro.id,'reputacao')
        await ctx.send(
            f" **{ctx.message.author}** Concendeu um ponto de reputação para **{membro}**\n"
            f"Reputação atual `{atual}`  pontos. "
        )

    @rep.error
    async def rep_error(self, ctx, error):
        """ Tratamento de erros do comando rep. Vamos colocar um mensagem quando o usuário estiver em colldown"""
        if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.send(f" **Exemplo** `{self.bot.prefixo}rep [Nome ou id do usuario]`")
            return
        if isinstance(error, discord.ext.commands.CommandOnCooldown):
            min, sec = divmod(error.retry_after, 60)
            h, min = divmod(min, 60)
            if min == 0.0 and h == 0:
                await ctx.send(f' **Espere `{round(sec)}` segundos . Para enviar pontos novamente.**')
            else:
                await ctx.send(f"**Espere `{round(h)}` horas `{round(min)}` minutos  e `{round(sec)}` segundos. Para enviar pontos novamente**")

    @commands.command()
    @commands.cooldown(1, 43200, commands.BucketType.user)
    async def diario(self, ctx):
        _user = ctx.message.author.id
        db.verificar(_user)
        valor = 100
        db.setar_moedas(_user,valor)
        _atual = db.buscar(_user,'moedas')
        await ctx.send(f"{ctx.message.author.mention} Acabou de Ganhar `100` moedas\nAtualmente possui `{_atual}` moedas")

    @diario.error
    async def diario_error(self, ctx, error):
        """ Tratamento de erros do comando diario. Vamos colocar um mensagem quando o usuário estiver em colldown"""
        if isinstance(error, discord.ext.commands.CommandOnCooldown):
            min, sec = divmod(error.retry_after, 60)
            h, min = divmod(min, 60)
            if min == 0.0 and h == 0:
                await ctx.send(f' **Espere `{round(sec)}` segundos . Para ganhar o bonûs diário novamente.**')
            else:
                await ctx.send(f"**Espere `{round(h)}` horas `{round(min)}` minutos  e `{round(sec)}` segundos. Para ganhar o bonûs diário novamente")


# Funcão de setup do cog
def setup(bot):
    bot.add_cog(economia(bot))