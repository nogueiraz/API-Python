import tkinter 
from random import *
import os
import time
import psutil
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from conexaoBanco import criar_conexao
from comando import dadosSendoInseridos
import pandas as pd
import datetime as dt
import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt



arrayConsumoRAM = [0] * 10 
arrayConsumoCPU = [0] * 10

dispositivo= psutil.disk_partitions()
cores = '#add8e6','#00008b'
armzDisco = psutil.disk_usage(dispositivo[0][0])
armzDiscoUsado = armzDisco.used / 1024 / 1024 / 1024
armzDiscototal = armzDisco.total / 1024 / 1024 / 1024
armzDiscoDispobivel = armzDiscototal - armzDiscoUsado


conexao = criar_conexao("localhost","root","", "dados_de_maquinateste")

def transformarEmCsv() :
    cursor = conexao.cursor()
    sql = "SELECT consumoRAM_PercentTeste , consumoCPU_PercentTeste FROM teste1;"
    cursor.execute(sql)

    resultado = cursor.fetchall()
    RAM = []
    CPU = []
   
    
    for consumoRAM_PercentTeste, consumoCPU_PercentTeste in resultado:
        RAM.append(consumoRAM_PercentTeste)
        CPU.append(consumoCPU_PercentTeste)
    

    dic = {"RAM":RAM,"CPU":CPU}
    df = pd.DataFrame(dic)
    df.to_csv("C:DadosColetados"+str( dt.date.today() )+".csv")

def ApertarBotao3():
    cursor = conexao.cursor()
    sql = "SELECT consumoRAM_PercentTeste , consumoCPU_PercentTeste FROM teste1;"
    cursor.execute(sql)

    resultado = cursor.fetchall()
    todaRam = []
    todaCpu = []
   
    
    for consumoRAM_PercentTeste, consumoCPU_PercentTeste in resultado:
        todaRam.append(consumoRAM_PercentTeste)
        todaCpu.append(consumoCPU_PercentTeste)

    janela3 = tkinter.Tk()
    janela3.title("Dados Coletados")
    
    janela3.configure(background='black')
    larguraScreen = janela3.winfo_screenwidth()
    alturaScreen = janela3.winfo_screenheight()
    posx = larguraScreen/2 - 250
    posy = alturaScreen/2 - 250 
    janela3.geometry("600x500+%d+%d" % (posx, posy))

    botaoVoltar = tkinter.Button(janela3, text="Voltar", command=janela3.destroy)
    botaoVoltar.place(x=10, y=7)
    botaoVoltar.configure(background='white', foreground='black', font=('arial', 15, 'bold'))
    
    graficoDestalhadoCPU = plt.figure(figsize=(3,3))
    canva = FigureCanvasTkAgg(graficoDestalhadoCPU, master=janela3)
    canva.get_tk_widget().place(x=0, y=60)
    graficoDestalhadoCPU.suptitle("Consumo de CPU")
    graficoDestalhadoCPU.add_subplot(111).plot(todaCpu)

    graficoDestalhadoRAM = plt.figure(figsize=(3,3))
    canva = FigureCanvasTkAgg(graficoDestalhadoRAM, master=janela3)
    canva.get_tk_widget().place(x=290, y=60)
    graficoDestalhadoRAM.suptitle("Consumo de RAM")
    graficoDestalhadoRAM.add_subplot(111).plot(todaRam)
    

    tkinter.mainloop()


def ApertarBotao2():
   
    transformarEmCsv()

    leitura = pd.read_csv("C:DadosColetados"+str( dt.date.today() )+".csv")
    leitura = leitura.drop("Unnamed: 0", axis=1)

        
    wc = WordCloud(background_color="white", max_words=1000, width=800, height=400)
    print(str(leitura))
    wc.generate(str(leitura))
    plt.imshow(wc)
    plt.axis("off")
    plt.show()
  
    
def ApertarBotao():
        janela2 = tkinter.Tk()
        janela2.title("Dashboard")
        larguraScreen = janela2.winfo_screenwidth()
        alturaScreen = janela2.winfo_screenheight()
        posx = larguraScreen/2 - 250
        posy = alturaScreen/2 - 250 
        janela2.geometry("530x500"+"+%d+%d" % (posx, posy))


        textoDash = tkinter.Label(janela2, text="Dashboard")
        textoDash.config(font=("Arial", 15),background="black", foreground="white")
        textoDash.place(x=200, y=0)    


        labels = f'Usado - {round(armzDiscoUsado)} Gb', f'Disponível - {round(armzDiscoDispobivel)} Gb' 
        sizes = [((armzDiscoUsado/armzDiscototal)*100), ((armzDiscoDispobivel/armzDiscototal)*100)] 
        figura = plt.figure(figsize=(2,3), dpi=100)
        canva = FigureCanvasTkAgg(figura,janela2 )
        canva.get_tk_widget().place(x=310,y=30)


        graficosUnidArmz=figura.add_subplot(111)
        graficosUnidArmz.pie(sizes, autopct='%1.1f%%', startangle=0, colors = cores) 
        graficosUnidArmz.title.set_text(f'Unidade - {dispositivo[0][0]}') 
        graficosUnidArmz.legend(labels, loc="best", bbox_to_anchor=((0.6, -0.3, 0.5, 0.5))) 
        graficosUnidArmz.axis('equal')       


        while True:
            arrayConsumoRAM.append(psutil.virtual_memory()[2]) 
            arrayConsumoRAM.remove(arrayConsumoRAM[0]) 
            arrayConsumoCPU.append(psutil.cpu_percent(interval=None))
            arrayConsumoCPU.remove(arrayConsumoCPU[0]) 


            
       
            figura = plt.figure(figsize=(3,2), dpi=100)
            graficoRam = figura.add_subplot(111)
            canva2= FigureCanvasTkAgg(figura,janela2 )
            canva2.get_tk_widget().place(x=0,y=240)


            figura = plt.figure(figsize=(3,2), dpi=100)
            graficoCPU = figura.add_subplot(111)
            canva= FigureCanvasTkAgg(figura,janela2 )
            canva.get_tk_widget().place(x=0,y=30)


            graficoCPU.plot(arrayConsumoCPU, color='blue', label='Consumo de RAM')
            graficoCPU.scatter(len(arrayConsumoCPU) - 1, arrayConsumoCPU[-1], color='blue')
            graficoCPU.title.set_text(f'Consumo de CPU - {arrayConsumoCPU[-1]}%')
            graficoCPU.set_ylim(0, 100)


            graficoRam.plot(arrayConsumoRAM, color='red', label='Consumo de RAM')
            graficoRam.scatter(len(arrayConsumoRAM) - 1, arrayConsumoRAM[-1], color='red')
            graficoRam.title.set_text(f'Consumo de RAM - {arrayConsumoRAM[-1]}%')
            graficoRam.set_ylim(0, 100)

            conCPU = arrayConsumoCPU[-1]
            conRAM = arrayConsumoRAM[-1]
            dados = str(conCPU) + ","+ str(conRAM) + ");"

            dadosSendoInseridos(conexao, dados)
            
            janela2.configure(background="black")


            janela2.update()
            time.sleep(2)
             
            
          

janela = tkinter.Tk()
janela.title("Teste")
janela.configure(background="black")


larguraScreen = janela.winfo_screenwidth()
alturaScreen = janela.winfo_screenheight()
posx = larguraScreen/2 - 250
posy = alturaScreen/2 - 250 


janela.geometry("500x500"+"+%d+%d" % (posx, posy))


janela.configure(background="black")

imagemHcs = tkinter.PhotoImage(file="hcs2e.png")
imagelLabelHcs = tkinter.Label(janela, image=imagemHcs)
imagelLabelHcs.place(x=100, y=100)
imagelLabelHcs.configure(background="white")



imagemBotao = tkinter.PhotoImage(file="button_dashboard.png")
botao = tkinter.Button(janela, image= imagemBotao, command=ApertarBotao)
botao.place(x=270,y=250)
botao.config(bg="black" , bd=0)


imageBotao2 = tkinter.PhotoImage(file="button_wordcloud.png")
botao2 = tkinter.Button(janela, image= imageBotao2, command=ApertarBotao2)
botao2.place(x=80,y=250)
botao2.config(bg="black", bd=0)

imagemBotao3 = tkinter.PhotoImage(file="button_graficos.png")
botao3 = tkinter.Button(janela, image= imagemBotao3, command=ApertarBotao3)
botao3.place(x=190,y=350)
botao3.config(bg="black", bd= 0)


janela.mainloop()










