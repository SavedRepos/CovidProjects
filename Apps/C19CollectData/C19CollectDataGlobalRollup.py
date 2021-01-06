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

#global file_index
#global file_index_entry

COUNTRY_LOCATION = {
    'Australia'     : '-35.308056,149.124444',
    'Canada'        : '45.4,-75.666667',
    'China'         : '39.916667, 116.383333',
    'Denmark'       : '55.716667, 12.566667',
    'France'        : '48.85, 2.35',
    'Netherlands'   : '52.366667, 4.883333',
    'United Kingdom': '51.507222, -0.1275'
}

def processProvinceRollup(df):
    
    # 6 Find countries with province data only and create a country rollup
    
    count = 0
    last_country = ''
    global_new_keys = []

    dfPopulations = pd.read_csv(cd.WORLD_POP)
    
    global_keys = df.Combined_Key.unique()
    for new_key in global_keys:
        words = new_key.split(', ')
        if words[0] != "":
            if words[1] != last_country:
                global_new_keys.append(words[1])
        last_country = words[1]

        count += 1

    # 7 Create a country by rolling up data
    for key in global_new_keys:
        lat_long = COUNTRY_LOCATION[key].split(',')
        #dfx = pd.DataFrame(columns = ['Province','Country','Lat','Long','Date','Confirmed','Deaths','Key'])
        
        dfa = df[df['Country_Region'] == key].copy()
        grp = dfa.groupby(by=['Date'], as_index=False).agg({'Confirmed' : ['sum'], 'Deaths' : ['sum']} )
        rows = []
        i = 0
        for idx, row in grp.iterrows():
            province     = ''
            country      = key
            lat          = lat_long[0]
            long         = lat_long[1]
            date         = row['Date'].values[0] 
            date         = np.datetime_as_string(date, unit='D')
            try:
                #print(dfPopulations)
                pop = dfPopulations[cd.dfPopulations['Country'] == key]
                population = pop['Population'].values[0]
            except:
                population = 0
                logging.error(f'ERROR: Global Other No population for {key}')
            confirmed    = row['Confirmed'].values[0]   
            deaths       = row['Deaths'].values[0]   
            combined_key = key
            thisRow      = [province, country, lat, long, date, population, confirmed, deaths, combined_key]
            rows.append(thisRow)
            i += 1

        dfx = pd.DataFrame(rows, columns = ['Province_State','Country_Region','Lat','Long','Date','Population','Confirmed','Deaths','Combined_Key'])
        dfx = dfx.sort_values(['Date'], ascending=[True])
        #dfx['Country']          = dfKey
        #dfx['Province']         = ''
        #dfx['Lat']              = lat_long[0]
        #dfx['Long']             = lat_long[1]
        #dfx['Key']              = dfKey + ' / '
        dfx['ConfirmedNew'] = dfx['Confirmed'].diff()
        dfx['DeathsNew'] = dfx['Deaths'].diff()
        dfx['ConfirmedNewMean'] = dfx['ConfirmedNew'].rolling(7).mean()
        dfx['DeathsNewMean'] = dfx['DeathsNew'].rolling(7).mean()
        dfx['Population'] = 0
        dfx.drop(dfx.index[[0,1,2,3,4,5,6]])
        #print(dfx.head(n=10))

        file_name = dfa['Country_Region'].values[0] + '.csv'
        file_name = file_name.replace(',', '')
        file_name = file_name.replace('*', '')
        file_path = os.path.join(cd.CSV_DIRECTORY, file_name)
        dfx.to_csv(file_path, index=False)

        cd.file_index.append(
            cd.file_index_entry(dfx['Combined_Key'].values[0],
                                file_name,
                                dfx['Country_Region'].values[0],
                                dfx['Province_State'].values[0] 
            )
        )
        
    return df

