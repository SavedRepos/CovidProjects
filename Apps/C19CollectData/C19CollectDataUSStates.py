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

import C19CollectDataMain as cd

#global file_index
#global file_index_entry

# Prepare US dataframe
# ----------------------------------------------------------------------------

def processUSDataframe():
    ''' Processing the US dataframe '''

    logging.info('Processing U.S. csv files')

    # 1. Load confirmed dataframe
    # UID,iso2,iso3,code3,FIPS,Admin2,Province_State,Country_Region,Lat,Long_,Combined_Key
    dfConfirmed = pd.read_csv(cd.CONFIRMED_US)
    dfConfirmed = dfConfirmed.drop(['UID','iso2','iso3','code3','FIPS','Admin2', 'Combined_Key'], axis=1)
    dfConfirmed = pd.melt(dfConfirmed, id_vars=['Province_State','Country_Region','Lat','Long_'], var_name="Date", value_name="Confirmed")
    dfConfirmed = dfConfirmed.replace(np.nan, '', regex=True)
    dfConfirmed = dfConfirmed.rename(columns={"Value": "Confirmed"})

    # 2. Load deaths dataframe
    # UID,iso2,iso3,code3,FIPS,Admin2,Province_State,Country_Region,Lat,Long_,Combined_Key,Population
    dfDeaths = pd.read_csv(cd.DEATHS_US)
    dfDeaths = dfDeaths.drop(['UID','iso2','iso3','code3','FIPS','Admin2'], axis=1)
    dfDeaths = pd.melt(dfDeaths, id_vars=['Province_State','Country_Region','Lat','Long_', 'Combined_Key', 'Population'], var_name="Date", value_name="Deaths")
    dfDeaths = dfDeaths.replace(np.nan, '', regex=True)
    dfDeaths = dfDeaths.rename(columns={"Value": "Deaths"})
    
    # 3. Merge confirmed and deaths dataframes
    df = pd.merge(dfConfirmed, dfDeaths, on=['Province_State', 'Country_Region', 'Lat', 'Long_', 'Date'])
    df = df.rename(columns={'Long_': 'Long'})
    df = df.replace(np.nan, '', regex=True)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values(['Country_Region', 'Province_State', 'Date'])

    i = 0
    app = Nominatim(user_agent="tutorial")
    states = pd.unique(dfDeaths['Province_State'].values.ravel())
    for state in states:
        # if state.endswith('Princess'):
        #     logging.error('Bypassing:', state)
        #     continue
        #print('State:',state)
        dfState = df[df['Province_State'] == state] 
        location = app.geocode(state).raw
        grp = df.groupby(by=['Date'], as_index=False).agg({'Confirmed' : ['sum'], 'Deaths' : ['sum'], 'Population' : ['sum']} )

        rows = []
        i = 0
        for idx, row in grp.iterrows():
            province     = state
            country      = 'US'
            lat          = location['lat']
            long         = location['lon']
            date         = row['Date'].values[0] 
            date         = np.datetime_as_string(date, unit='D')
            population   = row['Population'].values[0]
            confirmed    = row['Confirmed'].values[0]   
            deaths       = row['Deaths'].values[0]   
            combined_key = province + ', US'
            thisRow      = [province, country, lat, long, date, population, confirmed, deaths, combined_key]
            rows.append(thisRow)
            i += 1

        dfs = pd.DataFrame(rows, columns = ['Province_State','Country_Region','Lat','Long','Date','Population','Confirmed','Deaths','Combined_Key'])
        dfs = dfs.sort_values(['Date'], ascending=[True])
        dfs['ConfirmedNew'] = dfs['Confirmed'].diff()
        dfs['DeathsNew'] = dfs['Deaths'].diff()
        dfs['ConfirmedNewMean'] = dfs['ConfirmedNew'].rolling(7).mean()
        dfs['DeathsNewMean'] = dfs['DeathsNew'].rolling(7).mean()
        dfs.drop(dfs.index[[0,1,2,3,4,5,6]])

        file_name = dfs['Province_State'].values[0] + '.csv'
        file_name = file_name.replace(',', '')
        file_name = file_name.replace('*', '')
        file_path = os.path.join(cd.CSV_DIRECTORY, file_name)
        dfs.to_csv(file_path, index=False)

        cd.file_index.append(
            cd.file_index_entry(dfs['Combined_Key'].values[0],
                                file_name,
                                dfs['Country_Region'].values[0],
                                dfs['Province_State'].values[0] 
            )
        )

    return df

