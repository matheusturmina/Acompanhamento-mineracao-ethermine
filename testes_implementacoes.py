import time as tm
import datetime

import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


#Achando os valores na página WEB
#Configurando o browser para abrir minimizado
options = webdriver.ChromeOptions()
#Desabilitando os print de devtools
options.add_experimental_option('excludeSwitches', ['enable-logging'])

#inicializando ele
driver = webdriver.Chrome("C:/chromedriver.exe",chrome_options=options)

driver.get("https://minerstat.com/coin/ETH")
tm.sleep(5)
#achando os valores
epoch = driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[1]/div[1]/div[8]/div[2]/b').text
print (epoch)

