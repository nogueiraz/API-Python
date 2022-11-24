import mysql.connector

def criar_conexao (host,usuario,senha,nomeBD):
    conexao = mysql.connector.connect(host=host,user=usuario,password=senha,database=nomeBD)
    return conexao

def fechar_conexao(conexao):
    conexao.close()

