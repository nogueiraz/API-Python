
def dadosSendoInseridos(conexao, dados):
    cursor = conexao.cursor()
    sql = "INSERT INTO teste1 (consumoCPU_PercentTeste, consumoRAM_PercentTeste) VALUES (" + dados
    cursor.execute(sql)
    conexao.commit()
    




    








