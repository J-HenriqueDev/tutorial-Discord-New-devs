# Importações
from discord.ext import commands
import discord
from config import setup

class main(commands.AutoShardedBot):
    def __init__(self):
        """ Dentro do init vão alguns parâmetro que você pode encontrar nesse link :https://discordpy.readthedocs.io/en/rewrite/api.html """
        super().__init__(command_prefix=setup.PREFIXO,
                         pm_help=None,
                         description="vagner tutorial",
                         )
        self.prefixo = setup.PREFIXO
        # Vamos carregar o cogs da pasta.
        for cog in setup.COGS:
            try:
               self.load_extension(cog)
               print(f"Arquivo {cog} carregado com sucesso.")
            # Não é um boa pratica fazer esse tipo de tratamento de erro
            # Os erros que essa função retorna são: ExtensionNotFound,ExtensionAlreadyLoaded,NoEntryPointError  e ExtensionFailed.
            except Exception as e:
                print(f"erro ao carregar o cog: {e} ")


    async def on_ready(self):
        """ Evento que dispara quando o bot for iniciado com sucesso"""
        print(f"{self.user.name} ONLINE - id:  {self.user.id}")
        await self.change_presence(activity=discord.Activity(name=f'News Dev tutorial', type=discord.ActivityType.watching))


    def logar(self):
        """ Funcão de login do bot"""
        try:
            super().run(setup.TOKEN, bot=True, reconnect=True)
        except Exception as e:
            print(f"Erro ao logar o bot: {e} ")

 # para checar o escopo e rodar a aplicação
if __name__ == '__main__':
  bot = main()
  bot.logar()