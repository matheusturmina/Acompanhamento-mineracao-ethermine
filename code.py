import time as tm
import datetime

import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

#Funcao para transformar diferença de datas em segundos
def dataToSeconds(data):
    #transformando dias em segundos
    diasEmSegundos = data.days * 86400
    totalSegundos = diasEmSegundos + data.seconds

    return totalSegundos

#funcao para transformar dados de dia e hora para a funcao datetime conseguir ler
def strToDate(stringData, stringHora):
    dia = int(stringData[0] + stringData[1])
    mes = int(stringData[3] + stringData[4])
    ano = int(stringData[6] + stringData[7] + stringData[8] + stringData[9])
    hora = int(stringHora[0] + stringHora[1])
    minuto = int(stringHora[3] + stringHora[4])
    segundo = int(stringHora[6] + stringHora[7])

    return datetime.datetime(ano, mes, dia, hora, minuto, segundo)

contador = 0
repetir = 'sempre'

while(repetir == 'sempre'):

    #Achando os valores na página WEB
    #Configurando o browser para abrir minimizado
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    #Desabilitando os print de devtools
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    #inicializando o driver do navegador
    driver = webdriver.Chrome("C:/chromedriver.exe",options=options)

    #Abrindo o site da ethermine
    driver.get("https://ethermine.org/miners/93aa493D6e139fc3db5e0673Fe6A60F1D283C723/dashboard")
    tm.sleep(5)

    #achando valores na ethermine
    unpaidBalance = driver.find_element_by_class_name('current-balance').text
    estimatedEarnings = driver.find_element_by_class_name('current-earnings').text
    realEarnings = ''
    currentHashrate = driver.find_elements_by_class_name('stat-card-body')[0].text
    averageHashrate = driver.find_elements_by_class_name('stat-card-body')[1].text
    reportedHashrate = driver.find_elements_by_class_name('stat-card-body')[2].text
    validShares = driver.find_elements_by_class_name('stat-card-body')[3].text
    staleShares = driver.find_elements_by_class_name('stat-card-body')[4].text
    invalidShares = driver.find_elements_by_class_name('stat-card-body')[5].text
    time = datetime.datetime.now().strftime("%H:%M:%S")
    date = datetime.datetime.now().strftime("%d/%m/%Y")

    #Mudando o site para o minerstat
    driver.get("https://minerstat.com/coin/ETH")
    tm.sleep(5)

    #achando valores no minerstat
    epoch = driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[1]/div[1]/div[8]/div[2]/b').text

    #Fechando o browser
    driver.close()


    # PLANILHAS GOOGLE

    # Definindo escopo
    scope = ['https://spreadsheets.google.com/feeds']

    # Credenciais de acesso
    credentials = ServiceAccountCredentials.from_json_keyfile_name('token.json', scope)

    # Efetuando login
    gc = gspread.authorize(credentials)

    #Selecionando Planilha pelo id
    wks = gc.open_by_key('10frt9FF3LZp_vbUusoahP4MFzZVUCKqkNASBOmaSUoU')

    # Setando uma variavel para a pagina 0 da planilha
    worksheet = wks.get_worksheet(0)

    #Descobrindo quantas linhas existem na tabela
    proximaLinha = (len(worksheet.col_values(1)) + 1)

    #Calculando o realEarnings
    #Achando a hora anterior
    horaAnterior = worksheet.cell(len(worksheet.col_values(1)),11).value
    #Achando o dia anterior
    diaAnterior = worksheet.cell(len(worksheet.col_values(1)),12).value

    #Usando a funcao de converter a data para a biblioteca conseguir ler
    dataAnterior = strToDate(diaAnterior,horaAnterior)
    dataAtual = datetime.datetime.now()
    diferencaDatas = dataAtual - dataAnterior
    if (3540 < dataToSeconds(diferencaDatas) < 3660):
        # Calculando o ganho real por dia, de acordo com a hora que passou
        unpaidBalanceAnterior = worksheet.cell(len(worksheet.col_values(1)),1).value
        diferencaBalances = (float(unpaidBalance) - float(unpaidBalanceAnterior))
        realEarnings = diferencaBalances*24

    #Adicionando os valores na próxima linha
    worksheet.update_cell((proximaLinha), 1, unpaidBalance)
    worksheet.update_cell((proximaLinha), 2, estimatedEarnings)
    worksheet.update_cell((proximaLinha), 3, realEarnings)
    worksheet.update_cell((proximaLinha), 4, currentHashrate)
    worksheet.update_cell((proximaLinha), 5, averageHashrate)
    worksheet.update_cell((proximaLinha), 6, reportedHashrate)
    worksheet.update_cell((proximaLinha), 7, validShares)
    worksheet.update_cell((proximaLinha), 8, staleShares)
    worksheet.update_cell((proximaLinha), 9, invalidShares)
    worksheet.update_cell((proximaLinha), 10, epoch)
    worksheet.update_cell((proximaLinha), 11, time)
    worksheet.update_cell((proximaLinha), 12, date)
    contador += 1

    print('Execução numero {}'.format(contador) + ' - ' + datetime.datetime.now().strftime("%H:%M"))
    tm.sleep(3600)


#REFERENCIAS https://www.linkedin.com/pulse/manipulando-planilhas-do-google-usando-python-renan-pessoa/?originalSubdomain=pt