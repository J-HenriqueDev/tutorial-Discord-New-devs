from discord.ext import commands
import discord
from config import setup



# Lembre sempre de colocar o commnads.Cog
class informacao(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def emojiinfo(self, ctx, *, emoji: discord.Emoji):
        """ Comando que vai buscar informações do emoji """
        emoji_embed = discord.Embed()
        emoji_embed.add_field(name="Nome",value=emoji.name)
        emoji_embed.add_field(name="Servidor", value=emoji.guild)
        emoji_embed.add_field(name="Id", value=emoji.id)
        emoji_embed.add_field(name="Animado", value=emoji.animated)
        emoji_embed.add_field(name="Gerenciando", value=emoji.managed)
        emoji_embed.add_field(name="Criado em", value=emoji.created_at.strftime('%d.%m.%Y %H:%M:%S %Z'))
        emoji_embed.add_field(name="Uso", value=f"<a:{emoji.name}:{emoji.id}>")
        emoji_embed.set_footer(text=f"{self.bot.user.name}", icon_url=self.bot.user.avatar_url)
        emoji_embed.set_thumbnail(url=emoji.url)
        await ctx.send(embed=emoji_embed)

    @emojiinfo.error
    async def emojiinfo_error(self, ctx, error):
        """ Tratamento de erros do emojiinfo quando não for encotrado o emoji ou não for passado com parâmetro no comando"""
        if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.send(f" **Exemplo** `{self.bot.prefixo}emojiinfo [Nome ou id do emoji]`")
            return
        else:
            print(error)
            await ctx.send(f" **Emoji não encontrado**")


# Funcão de setup do cog
def setup(bot):
    bot.add_cog(informacao(bot))