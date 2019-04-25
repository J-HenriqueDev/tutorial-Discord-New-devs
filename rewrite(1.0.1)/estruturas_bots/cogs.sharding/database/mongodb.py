from pymongo import MongoClient
from config import setup

try:
 client = MongoClient(setup.MONGO_URI)
 db = client.meubot.usuario
 print(f'mongodb on')
except Exception as e:
 print(f'mongodb off: {e}')

def novo_usuario(membro_id):
    """ Vai criar um novo usário. """
    user = {
        'id': membro_id,
        'moedas': 0,
        'reputacao':0
    }
    return db.insert_one(user)


def verificar(usuario_id):
    """ Vai verificar se o usuário já está salvo, se não vai chamar o função novo_usuario() e cria um novo registro."""
    _user = db.find_one({'id':usuario_id})
    if _user == None:
        novo_usuario(usuario_id)
    else:
        return True


def setar_moedas(usuario_id,moedas):
    """ Vai setar as moedas do usário. O operado $inc é do mongodb para incrementar.
        Parâmetros:
           usuario_id : o id do usário do servidor, tem que ser int.
    """
    user = {
        'id':usuario_id
    }
    moedas = {
       "$inc":{
           "moedas":moedas
       }
    }
    return db.update_one(user,moedas)


def setar_reputacao(usuario_id,pontos_rep):
    """ Vai setar os pontos do usário. O operado $set é do mongodb para reescrever.
       Parâmetros:
           usuario_id : o id do usário do servidor, tem que ser int.
    """
    user = {
        'id':usuario_id
    }
    reps = {
       "$set":{
           "reputacao":pontos_rep
       }
    }
    return db.update_one(user,reps)


def buscar(usuario_id,chave):
    """ Para buscar o usuario.
        Parâmetros:
           usuario_id : o id do usário do servidor, tem que ser int.
           chave : o valor de busca no banco no momento moedas ou reputação tem que ser string.
           exemplo: buscar(id,"coins")
    """
    _user = db.find_one({'id':usuario_id})
    _buscar = _user[f'{chave}']
    if _buscar == None:
        return False
    else:
        return _buscar