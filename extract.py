
from PyPDF2 import PdfFileReader, PdfFileWriter
from pathlib import Path
import word2vec
import re
from tkinter import filedialog
from tkinter import *
import tkinter as tk


def takeArk():
    arquivo = filedialog.askopenfilename()
    global nome_arquivo
    nome_arquivo = arquivo
    arquivo_selecionado["text"] = arquivo


def mainFunction():
    # INTERFACE
    # recebendo a palavra chave
    palavraChave = vpalavra.get()

    # Importando o arquivo PDF
    pdf = PdfFileReader(nome_arquivo);

    # Passos para extrair o texto
    # Passo 1 selecionar a pagina
    page_1_oject = pdf.getPage(0)

    # Passo 2 extrair o texto
    page_1_text = page_1_oject.extractText()

    # Combinar todas as paginas e salvar como txt
    with Path('docsEntrada/TXT_Gerado.txt').open(mode='w') as output_file:
        text = ''
        for page in pdf.pages:
            text += page.extractText()
        output_file.write(text.lower())

    # Entrando uma palavra no word2vec e ele processa e retorna um array de palavras similares, assim expandindo a capacidade da busca
    print("Processando...")
    word = word2vec.input(palavraChave)
    # teste = [["teste"], ["documento"]]
    print("Palavras geradas atraves da palavra incerida")
    with Path('gerados/Sentencas_encontradas.txt').open(mode='w') as output_file_3:
        output_file_3.write("")
    for w in word:
        palavra = w[0]
        palavra = palavra.replace('-', '')
        print(palavra)
        array_pages = []

        for page in pdf.pages:
            page_num = page['/StructParents']
            page_text = page.extractText()
            if palavra in page_text:
                array_pages.append(page_num)

        pdf_writer = PdfFileWriter()

        # Pegando o texto das paginas onde encontrou a palavra
        if (len(array_pages) > 0):
            # Obtendo a sentensa e o numero da pagina
            # Array de sentencas
            array_sentences = []
            for page in pdf.pages:
                page_num = page['/StructParents']  # se quiser saber o numero da paginas
                page_text = page.extractText()

                if palavra in page_text:
                    sentence_list = ['Palavra {} encontrada na pagina-> '.format(palavra.upper()) + str(page_num) + ': ' + sentence.replace('\n', '') for sentence in
                                     re.split('\. |\? |\!', page_text) if palavra in sentence][0]
                    array_sentences.append(" ")
                    array_sentences.append(sentence_list + '\n')

            text = '\n'.join(array_sentences)
            with Path('gerados/Sentencas_encontradas.txt').open(mode='a') as output_file_3:
                output_file_3.write(text)
                text_widget.insert(tk.END, text)
        else:
            pass


janela = Tk()
janela.geometry("720x820")
janela.title("Extrator de textos")
janela.configure(background="#4682B4")
centro = 110

texto_orientacao = Label(janela, background="#4682B4", font="arial",
                         text="Selecione o arquivo pdf onde deseja realizar a busca")
texto_orientacao.place(x=centro, y=20)

nome_arquivo = ""

selectArq = Button(janela, width=20, background="#87CEFA", font="arial", text="Selecionar o arquivo", command=takeArk)
selectArq.place(x=centro, y=50)

label_arquivo_selecionado = Label(janela, background="#4682B4", font="arial", text="Arquivo selecionado")
label_arquivo_selecionado.place(x=centro, y=100)

arquivo_selecionado = Label(janela, background="#4682B4", text="Endereco do arquivo selecionado:")
arquivo_selecionado.place(x=centro, y=120)

label_seleciona_palavra = Label(janela, background="#4682B4", font="arial", text="Palavra chave")
label_seleciona_palavra.place(x=centro, y=145)

vpalavra = Entry(janela)
vpalavra.place(x=centro, y=170, width=150, height=22.5)

label_sentencas = Label(janela, background="#4682B4", font="arial", text="Sentencas encontradas")
label_sentencas.place(x=centro, y=200)

text_widget = tk.Text(janela, height=5, width=40)
scroll_bar = tk.Scrollbar(janela)

text_widget.place(x=centro, y=230, width=500, height=480)

button_busca_semantica = Button(janela, text="Busca Semantica", background="#87CEFA", command=mainFunction)
button_busca_semantica.place(x=centro, y=720, width=100, height=40)

janela.resizable(False, False)
janela.mainloop()
