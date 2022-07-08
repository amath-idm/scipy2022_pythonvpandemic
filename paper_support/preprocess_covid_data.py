'''
Preprocess COVID data

Downloaded manually from https://ourworldindata.org/grapher/daily-covid-cases-deaths
'''

import pandas as pd
import sciris as sc

fn = 'daily-covid-cases-deaths.csv'
df = pd.read_csv(fn, parse_dates=['Day'])

df = df[df.Entity=='World']
df = df.rename(columns={'Day':'date', 'Daily new confirmed cases of COVID-19':'cases', 'Daily new confirmed deaths due to COVID-19':'deaths'})

sc.save('covid_cases_deaths.obj', df)

print('Done')