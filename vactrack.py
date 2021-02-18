# -*- coding: utf-8 -*-

# vactrack.py code by @thetafferboy

import pandas as pd
import tweepy
from datetime import datetime
from pandas_ods_reader import read_ods
import urllib.request

# # Twitter authorisation - you need to fill in your own API details (https://dev.twitter.com)
# auth = tweepy.OAuthHandler("consumer_key", "consumer_secret")
# auth.set_access_token("access_token", "access_token_secret")
# api = tweepy.API(auth)

# You can change population of UK if you wish, which will change % calculations
population_of_spain = 47332614

# How many blocks you want in progress bar, 15 works well with Twitter ▓▓▓▓▓░░░░░░░░░░
bar_total = 15
perc_per_bar = 100/bar_total

# This sets date to 2 days ago, as there is a lag in government data reporting. API requests will fail if you request date which has no data yet
from datetime import date, timedelta
date_to_check = date.today().isoformat()

# df = read_ods('https://www.mscbs.gob.es/profesionales/saludPublica/ccayes/alertasActual/nCov/documentos/Informe_Comunicacion_20210125.ods', "Hoja3")

today = date.today().strftime('%Y%m%d')
print(today)

baseurl = 'https://www.mscbs.gob.es/profesionales/saludPublica/ccayes/alertasActual/nCov/documentos/Informe_Comunicacion_'
full_url = baseurl + today + '.ods'

dataFile = 'data.ods'

urllib.request.urlretrieve(full_url, dataFile)

df = read_ods(dataFile, "Hoja3") # if anything is going to break...

number_of_vaccines_given = df.loc[19,'Dosis administradas (2)'] # or maybe this!
number_of_people_given_2_doses = df.loc[19,'Nº Personas vacunadas\n(pauta completada)']

number_of_people_given_1_dose = number_of_vaccines_given - number_of_people_given_2_doses

def BuildLoadingBars(vacines_given):
    perc_rounded = round( ((vacines_given / population_of_spain) * 100),2)

    solid_bars_to_print = int(perc_rounded // perc_per_bar)
    empty_bars_to_print = int(bar_total - solid_bars_to_print)

    dataToAdd =  '▓' * solid_bars_to_print
    dataToAdd += '░' * empty_bars_to_print
    dataToAdd += ' ' + str(perc_rounded) + '%\n\n'
    return dataToAdd

# def SendTweet(stringToTweet):
    # api.update_status(stringToTweet)

stringToTweet = 'A día '+ str(date_to_check)+ '\n\n'
stringToTweet += 'Personas que han recibido la 1ª vacuna: \n'
stringToTweet += BuildLoadingBars(number_of_people_given_1_dose)
stringToTweet += 'Personas que han recibido la 2ª vacuna: \n'
stringToTweet += BuildLoadingBars(number_of_people_given_2_doses)
stringToTweet += 'Según datos de @sanidadgob\n'
stringToTweet += '#VacunaCOVID19 #YoMeVacuno\n'
stringToTweet += 'https://www.mscbs.gob.es/profesionales/saludPublica/ccayes/alertasActual/nCov/vacunaCovid19.htm'

print(stringToTweet)
print(len(stringToTweet))

# SourceAndSendTweet(stringToTweet)
