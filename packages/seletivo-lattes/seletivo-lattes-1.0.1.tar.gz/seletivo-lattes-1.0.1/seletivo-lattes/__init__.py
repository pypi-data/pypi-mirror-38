# -*- coding: utf-8 -*-

#importar bibliotecas
import pandas as pd
import requests
from bs4 import BeautifulSoup
from time import sleep

#importar lista e lattes do arquivo listalattes.xlsx
#coluna 0 e link lattes
#coluna 1 e PPG ex GEAS
#caso tenha um PPG com M e D colocar PPG-M ou PPG-D ex PPGA-D
pd_lattes = pd.read_excel('listalattes.xlsx', header= None, index_col= None)   
list_lattes = pd_lattes[0]
PPG = pd_lattes[1]
print('Number of total CVs: ', len(list_lattes))

seletivo_df = pd.DataFrame()
for row in list_lattes:
    url = row
    page = requests.get(url)
    #Parse o HTML
    soup = BeautifulSoup(page.text, 'html.parser')
    #Achar nome do titular do CV Lattes
    name = soup.find(class_='nome')
    name = name.text
    #Achar a data de ultima atualização
    ultima_atualizacao = soup.find('ul', class_='informacoes-autor')
    ultima_atualizacao = ultima_atualizacao.text[-11:-1]
    #Achar Endereço Profissional
    #esse tal de layout-cell-pad-5 tem muitos no lattes
    layout_cell_pad_5 = soup.findAll('div', class_='layout-cell-pad-5')
    endereco_prof = layout_cell_pad_5[5].text
    #### ULTIMA FORMACAO###
    #Ano da ultima formacao
    ano_ultima_formacao = layout_cell_pad_5[6].text[1:-1]
    #Formacao TITULO e IES
    formacao = layout_cell_pad_5[7].text.split('\n')[0]
    formacao_titulo = formacao.split('.')[0]
    formacao_ies = formacao.split('.')[1]
    #Achar ultima atuacao profissional
    ultimo_vinculo = soup.findAll('div', class_='inst_back')[0]
    ultimo_vinculo_ies = ultimo_vinculo.text[1:].split('\n')[0]
    #Achar todos os artigos completos publicados em periodicos
    tb = soup.find_all('div', class_='artigo-completo') 
    #fazer uma lista com a quantidade de artigos completos
    prod = 0
    for i in tb:
        prod += 1
    new_df = pd.DataFrame(
    {'nome': name,
     'cv_lattes': list_lattes,
     'PPG': PPG,
     'ultima_atualizacao': ultima_atualizacao,
     'endereco_prof': endereco_prof,
     'ano_ultima_formacao': ano_ultima_formacao,
     'formacao_titulo': formacao_titulo,
     'formacao_ies': formacao_ies,
     'ultimo_vinculo_ies': ultimo_vinculo_ies,
     'prod_artigos_completos': prod
    }, index=[0])
    seletivo_df = seletivo_df.append(new_df, ignore_index=True)
    sleep(1) #esperar 1 segundo para cada requisicao

#exportar para Excel XLSX
seletivo_df.to_excel('seletivo_lattes.xlsx',index=False)
print('Done! You may now open the file seletivo_lattes.xlsx')
