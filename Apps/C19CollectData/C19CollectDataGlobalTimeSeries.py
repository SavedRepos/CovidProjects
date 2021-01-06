#!/usr/bin/env python3
#
# PrepareDataMain.py
#
# Prepare the data from Github and produce the csv files for other apps
#

from datetime import datetime
from dateutil.relativedelta import relativedelta
from dateutil import parser
from geopy.geocoders import Nominatim
import os
import logging
import numpy as np
import pandas as pd
import streamlit as st

import C19CollectDataMain as cd

global global_new_keys

#global file_index
#global file_index_entry

# ----------------------------------------------------------------------------
# Processing global dataframe
# ----------------------------------------------------------------------------

def processGlobalDataframe():
    ''' Prepare the global dataframe '''

    logging.info('Processing Global csv files')

    # 1. Load confirmed dataframe
    dfConfirmed = pd.read_csv(cd.CONFIRMED_GLOBAL)
    dfConfirmed = pd.melt(dfConfirmed, id_vars=['Province/State','Country/Region','Lat','Long'], var_name="Date", value_name="Confirmed")
    dfConfirmed = dfConfirmed.replace(np.nan, '', regex=True)
    dfConfirmed = dfConfirmed.rename(columns={"Value": "Confirmed"})

    # 2. Load deaths dataframe
    dfDeaths = pd.read_csv(cd.DEATHS_GLOBAL)
    dfDeaths = pd.melt(dfDeaths, id_vars=['Province/State','Country/Region','Lat','Long'], var_name="Date", value_name="Deaths")
    dfDeaths = dfDeaths.replace(np.nan, '', regex=True)
    dfDeaths = dfDeaths.rename(columns={"Value": "Deaths"})

    # 3. Merge confirmed and deaths dataframes
    df = pd.merge(dfConfirmed, dfDeaths, on=['Province/State', 'Country/Region', 'Lat', 'Long', 'Date'])
    df = df.rename(columns={'Country/Region': 'Country_Region', 'Province/State': 'Province_State'})
    #df = df.replace(np.nan, '', regex=True)
    df['Date'] = pd.to_datetime(df['Date'])

    df['Country_Region'] = df['Country_Region'].map(lambda x: x.replace(',',''))
    df['Country_Region'] = df['Country_Region'].map(lambda x: x.replace('*',''))
    df['Province_State'] = df['Province_State'].map(lambda x: x.replace(',',''))

    df = df.sort_values(['Country_Region', 'Province_State', 'Date'])

    # 4. Add columns 
    df['Combined_Key'] = df['Province_State']  + ', ' + df['Country_Region']

    # df['ConfirmedNew'] = df['Confirmed'].diff()
    # df['DeathsNew'] = df['Deaths'].diff()
    # df['ConfirmedNewMean'] = df['ConfirmedNew'].rolling(7).mean()
    # df['DeathsNewMean'] = df['DeathsNew'].rolling(7).mean()
    # df['Population'] = 0
    # #df.drop(df.index[[0,1,2,3,4,5,6]])

    global_keys = df.Combined_Key.unique()
    for key in global_keys:
        key_words = key.split(', ')
        search_key = key_words[1]
        if key_words[0] != '':
            search_key = key_words[0]

        dfKey = cd.dfPopulations[cd.dfPopulations['Combined_Key'] == key]
        try:
            population = dfKey['Population'].values[0]
        except:
            population = 0
            logging.error(f'ERROR: Global No population for {key}')

        index = df.index[df['Combined_Key'] == key].tolist()
        for i in index:
            df.at[i, 'Population'] = population

    # 5 Write csv files
    for global_key in global_keys:
        dfa = df[df['Combined_Key'] == global_key].copy()

        dfa['ConfirmedNew'] = dfa['Confirmed'].diff()
        dfa['DeathsNew'] = dfa['Deaths'].diff()
        dfa['ConfirmedNewMean'] = dfa['ConfirmedNew'].rolling(7).mean()
        dfa['DeathsNewMean'] = dfa['DeathsNew'].rolling(7).mean()
        #dfa['Population'] = 0
        dfa.drop(dfa.index[[0,1,2,3,4,5,6]])


        file_name = dfa['Country_Region'].values[0] + '.csv'
        if dfa['Province_State'].values[0] == '':
            file_name = dfa['Country_Region'].values[0]
        else:
            file_name = dfa['Province_State'].values[0]
        file_name = file_name.replace(',', '')
        file_name = file_name.replace('*', '')
        file_spec = file_name  + '.csv'
        file_path = os.path.join(cd.CSV_DIRECTORY, file_spec)
        dfa.to_csv(file_path, index=False)

        iEntry = cd.file_index_entry(dfa['Combined_Key'].values[0],
                                     file_spec,
                                     dfa['Country_Region'].values[0],
                                     dfa['Province_State'].values[0] 
                                    )

        cd.file_index.append(iEntry)

    return df
