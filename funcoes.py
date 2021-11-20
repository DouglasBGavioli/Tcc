from PyPDF2 import PdfFileReader, PdfFileWriter
from pathlib import Path

import re

def criaTXT(arquivo, titulo):
    pdf = PdfFileReader('{}.pdf'.format(arquivo))
    # Dois passos para extrair o texto
    # Passo 1 selecionar a pagina
    page_1_oject = pdf.getPage(0)
    # Passo 2 extrair o texto
    page_1_text = page_1_oject.extractText()

    # Combinar todas as paginas e salvar como txt
    with Path('{}.txt'.format(titulo)).open(mode='w') as output_file:
        text = ''
        for page in pdf.pages:
            text += page.extractText()
        output_file.write(text)