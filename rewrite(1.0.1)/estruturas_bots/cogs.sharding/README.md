# Como iniciar o bot
na pasta config tem o arquivo setup.py <br>
nesse arquivo coloque seu token e o prefixo como o exemplo abaixo<br>
```
TOKEN = "o token do bot"
PREFIXO = "prefixo de comando do bot"
MONGO_URI = "link da sua database"
COGS = [aqui dentro vai os cogs para ser carregado ex: "cogs.ping"]
```
# Instalar as bibliotecas necessárias
tenha o [python](https://www.python.org/downloads/) instalado. <br>
abra o terminal e navegue para a pasta do seu projeto. <br>
vamos insolar o nosso ambiente de desenvolvimento do sistema . <br>
use o comando `pip install virtualenv` . <br>
após instalar use `virtualenv env` isso irá criar a pasta env.<br>
use os comando a seguir: `cd env` `cd  Scripts` e por fim `activate`.
pronto nossa virtual env está ativado, agora iremos instalar os pacotes.<br>
digite `pip install -r requirements.txt` no terminal.<br>
depois de instalar ainda no terminal digite `python main.py` .<br>
pronto agora o bot ficou on.<br>
