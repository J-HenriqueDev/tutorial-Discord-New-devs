from discord.ext import commands



# Lembre sempre de colocar o commnads.Cog
class ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @commands.command()
    async def ping(self, ctx):
        """ Estrutura básica de um comando"""
        pingTime = self.bot.latency
        ping1 = round(pingTime, 2)
        await ctx.send('🏓 pong `{}ms`'.format(ping1))



# Funcão de setup do cog
def setup(bot):
    bot.add_cog(ping(bot))