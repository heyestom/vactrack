# -*- coding: utf-8 -*-

# vactrack.py code by @thetafferboy

import sys
# import pandas as pd
import tweepy
from datetime import datetime
# from pandas_ods_reader import read_ods
import urllib.request

# # Twitter authorisation - you need to fill in your own API details (https://dev.twitter.com)
# auth = tweepy.OAuthHandler("consumer_key", "consumer_secret")
# auth.set_access_token("access_token", "access_token_secret")
# api = tweepy.API(auth)

# You can change population of UK if you wish, which will change % calculations
population_of_spain = 47332614



import tweepy

today = date.today().strftime('%Y%m%d')
print(today)

# calculate today's date and format it to match
# the ods file url from the .gob website
from datetime import date, timedelta
date_to_check = date.today()
today = date_to_check.strftime('%Y%m%d')
baseurl = 'https://www.mscbs.gob.es/profesionales/saludPublica/ccayes/alertasActual/nCov/documentos/Informe_Comunicacion_'
full_url = baseurl + today + '.ods'

# download and read today's data
# into a pandas data frame
import pandas
from pandas_ods_reader import read_ods

dataFile = 'data.ods'
urllib.request.urlretrieve(full_url, dataFile)
# Comunicación is a specifc sheet in the .ods dataFile
# This is quite brittle and if anything is going to break...
df = read_ods(dataFile, "Comunicación")


# read the data from the downloaded file also brittle
# but I'd sooner it break that tweet something wrong
number_of_vaccines_given = df.loc[20,'Dosis administradas (2)']
number_of_people_given_2_doses = df.loc[20,'Nº Personas vacunadas\n(pauta completada)']

print("Total vacs given: ")
print(number_of_vaccines_given)
print("Total given 2 doses: ")
print(+ number_of_people_given_2_doses)

number_of_people_given_1_dose = number_of_vaccines_given - number_of_people_given_2_doses

def handler(event, context):
    return 'Hello from AWS Lambda using Python' + sys.version + '!'

def BuildLoadingBars(vaccines_given):
    population_of_spain = 47332614
    # How many blocks you want in progress bar
    # 15 works well with Twitter ▓▓▓▓▓░░░░░░░░░░
    bar_total = 15
    perc_per_bar = 100 / bar_total

    perc_rounded = round( ((vaccines_given / population_of_spain) * 100),2)

    # floor / integer division you can't
    # have .5 of a char based loading bar
    solid_bars_to_print = int(perc_rounded // perc_per_bar)
    empty_bars_to_print = int(bar_total - solid_bars_to_print)

    # python lets you multiply chars and I think it is cute
    dataToAdd =  '▓' * solid_bars_to_print
    dataToAdd += '░' * empty_bars_to_print
    dataToAdd += ' ' + str(perc_rounded) + '%\n\n'
    return dataToAdd

def SendTweet(tweet):
    api.update_status(tweet)

tweet = 'A día '+ str(date_to_check.isoformat())+ '\n\n'
tweet += 'Personas que han recibido la 1ª vacuna: \n'
tweet += BuildLoadingBars(number_of_people_given_1_dose)
tweet += 'Personas que han recibido la 2ª vacuna: \n'
tweet += BuildLoadingBars(number_of_people_given_2_doses)
tweet += 'Según datos de @sanidadgob\n'
tweet += '#VacunaCOVID19 #YoMeVacuno\n'
tweet += 'https://www.mscbs.gob.es/profesionales/saludPublica/ccayes/alertasActual/nCov/vacunaCovid19.htm'

print(tweet)
print(len(tweet))

# SendTweet(tweet)
