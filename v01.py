# -*- coding: utf-8 -*-
"""
Spyder Editor - Robozinho v0

"""

# Rodar no terminal
# cd C:\Users\LeonardoTV.INSPER\Dropbox\Trab\Robozinho

import os
#os.getcwd()
os.chdir("/Users/Leonardo/Documents/Pasta/Dropbox/Trab/Robozinho")


# CODIGO PARA ABRIR O SITE DO TSE E VERIFICAR CASOS DE ELEITORES
# EM CADA MUNICIPIO AO LONGO DOS ANOS, POR FAIXA ETARIA
from selenium import webdriver
from selenium.webdriver.support.ui import Select
#from selenium.webdriver.common.keys import Keys
#import urllib.request
#from bs4 import BeautifulSoup
import pandas as pd

# Abre o driver no Google Chrome para o site do TSE
driver = webdriver.Chrome("chromedriver")
driver.get("http://www.tse.jus.br/eleitor/estatisticas-de-eleitorado/estatistica-do-eleitorado-por-sexo-e-faixa-etaria")
# Verifica se o site está correto (busca pela palavara "Estatísticas")
assert "Estatísticas"


# Redireciona a janela para o frame de interesse (tabela de consulta)
frame = driver.find_element_by_xpath('//*[@id="windowZ"]')
driver.switch_to_frame(frame)

# Cria verificador de tabela fora do loop
verifica_tabela = 1

# Gerar lista de anos
select_year1 = driver.find_element_by_xpath('//*[@id="P0_SLS_ANO_DIS_SF"]')
years = select_year1.find_elements_by_tag_name("option")
yearsList=[]
for year in years:
    yearsList.append(year.get_attribute("value")) 
    
for y in range(0,len(yearsList)):
    print(yearsList[y])
    select_year2 = Select(driver.find_element_by_xpath('//*[@id="P0_SLS_ANO_DIS_SF"]'))
    select_year2.select_by_value(yearsList[y])
    
    # Gerar lista de meses no ano
    select_month1 = driver.find_element_by_xpath('//*[@id="P0_SLS_MES_DIS_SF"]')
    months = select_month1.find_elements_by_tag_name("option")
    monthsList=[]
    for month in months:
        monthsList.append(month.get_attribute("value"))
    for m in range(0,len(monthsList)):
        print(monthsList[m])
        select_month2 = Select(driver.find_element_by_xpath('//*[@id="P0_SLS_MES_DIS_SF"]'))
        select_month2.select_by_value(monthsList[m])
        
        # Selecionar opcao de nivel municipal
        select_month2 = Select(driver.find_element_by_xpath('//*[@id="P0_SLS_ABRAN_DIS_SF"]'))
        select_month2.select_by_value("M")
        driver.implicitly_wait(3) 
        
        # Gerar lista de estados
        select_state1 = driver.find_element_by_xpath('//*[@id="P0_SLS_UF_DIS_SF"]')
        states = select_state1.find_elements_by_tag_name("option")
        statesList=[]
        for state in states:
            statesList.append(state.get_attribute("value"))   
        for s in range(1,len(statesList)):
            select_state2 = Select(driver.find_element_by_xpath('//*[@id="P0_SLS_UF_DIS_SF"]'))
            select_state2.select_by_value(statesList[s])
            driver.implicitly_wait(3)
            
            # Gerar lista de municipios para o estado em questao
            select_city1 = driver.find_element_by_xpath('//*[@id="P0_SLS_MUNICIPIO_DIS_SF"]')
            cities = select_city1.find_elements_by_tag_name("option")
            citiesList=[]
            citiesNames=[]
            for city in cities:
                citiesList.append(city.get_attribute("value"))
                citiesNames.append(city.text)
            for c in range(1,len(citiesList)):
                select_city2 = Select(driver.find_element_by_xpath('//*[@id="P0_SLS_MUNICIPIO_DIS_SF"]'))
                select_city2.select_by_value(citiesList[c])               
                driver.implicitly_wait(3)
                
                # Geraremos a tabela final com o comando do pandas de pegar
                # todas as tabelas do site analisado. Ele cria um vetor com 
                # todas as tabelas da pagina. Por algum motivo a tabela correta
                # é a sétima (dfs[7])
                dfs = pd.read_html(driver.page_source , header=0)
                df_temp = dfs[7]
                df_temp = df_temp.assign(ano=yearsList[y],mes=monthsList[m],estado=statesList[s],cidade=citiesNames[c])
                
                # Gera a tabela final (adiciona tabela cidade a cidade)
                # Primeira vez - gera dataframe, daí em diante, append                
                if verifica_tabela == 1:
                    df_overall = df_temp
                    verifica_tabela = 2
                elif verifica_tabela == 2:
                    df_overall = df_overall.append(df_temp, ignore_index=True)                                                   
                # CRIAR ESPERA PARA DAR TEMPO DA TABELA CARREGAR

df_overall.to_csv("ELEITORES_SEXO_PARCIAL.csv",index=True)