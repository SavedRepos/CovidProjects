#!/usr/bin/env python3

#
# C19CreateData.py
#
# C19CreateData 
# 1. Reads the Confirmed and Deaths data from Johns Hopkins
# 2. Calculate new cases and deaths
# 3. Calculate a 5 day rolling average  
# 4. Produce a csv for use in reporting
#

import csv
from datetime import datetime
from dateutil.relativedelta import relativedelta
from dateutil import parser
import numpy as np
import os
from numpy.core.einsumfunc import _parse_possible_contraction
from numpy.lib.function_base import append
import pandas as pd
from typing import ValuesView

testing = False

# Province/State,Country/Region,Lat,Long,Date,Value
confirmedURL = "https://data.humdata.org/hxlproxy/data/download/time_series_covid19_confirmed_global_narrow.csv?dest=data_edit&filter01=explode&explode-header-att01=date&explode-value-att01=value&filter02=rename&rename-oldtag02=%23affected%2Bdate&rename-newtag02=%23date&rename-header02=Date&filter03=rename&rename-oldtag03=%23affected%2Bvalue&rename-newtag03=%23affected%2Binfected%2Bvalue%2Bnum&rename-header03=Value&filter04=clean&clean-date-tags04=%23date&filter05=sort&sort-tags05=%23date&sort-reverse05=on&filter06=sort&sort-tags06=%23country%2Bname%2C%23adm1%2Bname&tagger-match-all=on&tagger-default-tag=%23affected%2Blabel&tagger-01-header=province%2Fstate&tagger-01-tag=%23adm1%2Bname&tagger-02-header=country%2Fregion&tagger-02-tag=%23country%2Bname&tagger-03-header=lat&tagger-03-tag=%23geo%2Blat&tagger-04-header=long&tagger-04-tag=%23geo%2Blon&header-row=1&url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_confirmed_global.csv"
deathsURL    = "https://data.humdata.org/hxlproxy/data/download/time_series_covid19_deaths_global_narrow.csv?dest=data_edit&filter01=explode&explode-header-att01=date&explode-value-att01=value&filter02=rename&rename-oldtag02=%23affected%2Bdate&rename-newtag02=%23date&rename-header02=Date&filter03=rename&rename-oldtag03=%23affected%2Bvalue&rename-newtag03=%23affected%2Binfected%2Bvalue%2Bnum&rename-header03=Value&filter04=clean&clean-date-tags04=%23date&filter05=sort&sort-tags05=%23date&sort-reverse05=on&filter06=sort&sort-tags06=%23country%2Bname%2C%23adm1%2Bname&tagger-match-all=on&tagger-default-tag=%23affected%2Blabel&tagger-01-header=province%2Fstate&tagger-01-tag=%23adm1%2Bname&tagger-02-header=country%2Fregion&tagger-02-tag=%23country%2Bname&tagger-03-header=lat&tagger-03-tag=%23geo%2Blat&tagger-04-header=long&tagger-04-tag=%23geo%2Blon&header-row=1&url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_deaths_global.csv"
recoveredURL = "https://data.humdata.org/hxlproxy/data/download/time_series_covid19_recovered_global_narrow.csv?dest=data_edit&filter01=explode&explode-header-att01=date&explode-value-att01=value&filter02=rename&rename-oldtag02=%23affected%2Bdate&rename-newtag02=%23date&rename-header02=Date&filter03=rename&rename-oldtag03=%23affected%2Bvalue&rename-newtag03=%23affected%2Binfected%2Bvalue%2Bnum&rename-header03=Value&filter04=clean&clean-date-tags04=%23date&filter05=sort&sort-tags05=%23date&sort-reverse05=on&filter06=sort&sort-tags06=%23country%2Bname%2C%23adm1%2Bname&tagger-match-all=on&tagger-default-tag=%23affected%2Blabel&tagger-01-header=province%2Fstate&tagger-01-tag=%23adm1%2Bname&tagger-02-header=country%2Fregion&tagger-02-tag=%23country%2Bname&tagger-03-header=lat&tagger-03-tag=%23geo%2Blat&tagger-04-header=long&tagger-04-tag=%23geo%2Blon&header-row=1&url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_recovered_global.csv"

csvFolder    = '/Users/paulhart/Documents/Development/CovidProjects/Data/CSV_Files'

if testing == True:
    csvFolder    = '/Users/paulhart/Dropbox/COVID-19/Data/Test'
    confirmedURL = "/Users/paulhart/Dropbox/COVID-19/Data/Confirmed.csv"
    deathsURL    = "/Users/paulhart/Dropbox/COVID-19/Data/Deaths.csv"

country_location = {
    'Australia'     : '-35.308056,149.124444',
    'Canada'        : '45.4,-75.666667',
    'China'         : '39.916667, 116.383333',
    'Denmark'       : '55.716667, 12.566667',
    'France'        : '48.85, 2.35',
    'Netherlands'   : '52.366667, 4.883333',
    'United Kingdom': '51.507222, -0.1275'
}

# ----------------------------------------------------------------------------
# Prepare the Johns-Hopkins data into a Pandas Dataframe
# ---------------------------------------------------------------z-------------

def prepare_dataframe():

    # ----------------------------------------------------------------------------
    # Load deaths and confirmed dataframes
    # ---------------------------------------------------------------z-------------

    print("Loading confirmed data")
    dfConfirmed = pd.read_csv(confirmedURL)
    dfConfirmed = dfConfirmed.rename(columns={"Value": "Confirmed"})

    print("Loading deaths data")
    dfDeaths    = pd.read_csv(deathsURL)
    dfDeaths    = dfDeaths.rename(columns={"Value": "Deaths"})

    # ----------------------------------------------------------------------------
    # Merge deaths and confirmed dataframes
    # ----------------------------------------------------------------------------

    print('Merging confirmed and deaths')
    # result = pd.merge(left, right, on=['key1', 'key2'])
    df = pd.merge(dfConfirmed, dfDeaths, on=['Province/State', 'Country/Region', 'Lat', 'Long', 'Date'])

    # ----------------------------------------------------------------------------
    # Prepare dataframe 
    # ----------------------------------------------------------------------------

    print('Preparing DataFrame')
    df = df.drop(df.index[0])
    df = df.replace(np.nan, '', regex=True)
    df['Confirmed'] = df['Confirmed'].astype(np.float64)
    df['Deaths'] = df['Deaths'].astype(np.float64)
    df = df.rename(columns={'Country/Region': 'Country', 'Province/State': 'Province'})
    df = df.sort_values(['Country','Province','Date'], ascending=[True, True, True])

    df['Key'] = (df['Country'] + ' / ' + df['Province'])

    return df

# ----------------------------------------------------------------------------
# Create an index file in csv format and a csv file for each country and state
# ----------------------------------------------------------------------------

def create_csvs(df):

    print('Creating CSVs')
    indexEntries = []
    index_header = ['Country', 'File', 'Lat', 'Long']
    #index.append(index_header)
    dfKeys = df.Key.unique()
    for dfKey in dfKeys:
        #print(dfKey)
        index_entry = process_key(dfKey, df)
        indexEntries.append(index_entry)

    dfOtherKeys = find_other_keys(dfKeys, df)

    i = 0
    for dfKey in dfOtherKeys:
        #print(dfKey)
        index_entry = process_other_key(dfKey, df)
        indexEntries.append(index_entry)

    dfIndex = pd.DataFrame(indexEntries, columns=index_header)
    dfIndex = dfIndex.sort_values(['Country'], ascending=[True])
    file_path = os.path.join(csvFolder, 'Index.csv')
    dfIndex.to_csv(file_path, index=False)

    print('Number of keys:', len(dfKeys))

# ----------------------------------------------------------------------------
# Process a key
# ----------------------------------------------------------------------------

def process_key(dfKey, df):
    dfa                     = df[df['Key'] == dfKey].copy()
    dfa['ConfirmedNew']     = dfa['Confirmed'].diff()
    dfa['DeathsNew']        = dfa['Deaths'].diff()
    dfa['ConfirmedNewMean'] = dfa['ConfirmedNew'].rolling(7).mean()
    dfa['DeathsNewMean']    = dfa['DeathsNew'].rolling(7).mean()
    file_name = dfa['Country'].values[0] + '.csv'
    if dfa['Province'].values[0] == '':
        file_name = dfa['Country'].values[0]
    else:
        file_name = dfa['Province'].values[0]
    file_name = file_name.replace(',', '')
    file_name = file_name.replace('*', '')
    file_spec = file_name  + '.csv'
    file_path = os.path.join(csvFolder, file_spec)
    dfa.to_csv(file_path, index=False)

    index_entry = [file_name, file_spec, dfa['Lat'].values[0], dfa['Long'].values[0]]

    return index_entry

# ----------------------------------------------------------------------------
# Process other key
# ----------------------------------------------------------------------------

def process_other_key(dfKey, df):
    # Province/State,Country/Region,Lat,Long,Date,Value
    #print(dfKey)

    lat_long                = country_location[dfKey].split(',')
    #dfx = pd.DataFrame(columns = ['Province','Country','Lat','Long','Date','Confirmed','Deaths','Key'])
    
    dfa                     = df[df['Country'] == dfKey].copy()
    grp                     = dfa.groupby(by=['Date'], as_index=False).agg({'Confirmed' : ['sum'], 'Deaths' : ['sum']} )
    rows = []
    i = 0
    for idx, row in grp.iterrows():
        province  = ''
        country   = dfKey
        lat       = lat_long[0]
        long      = lat_long[1]
        date      = row['Date'].values[0]
        confirmed = row['Confirmed'].values[0]   
        deaths    = row['Deaths'].values[0]   
        key       = dfKey + ' / '
        thisRow   = [province, country, lat, long, date, confirmed, deaths, key]
        rows.append(thisRow)
        i += 1

    dfx = pd.DataFrame(rows, columns = ['Province','Country','Lat','Long','Date','Confirmed','Deaths','Key'])
    dfx                     = dfx.sort_values(['Date'], ascending=[True])
    #dfx['Country']          = dfKey
    #dfx['Province']         = ''
    #dfx['Lat']              = lat_long[0]
    #dfx['Long']             = lat_long[1]
    #dfx['Key']              = dfKey + ' / '
    dfx['ConfirmedNew']     = dfx['Confirmed'].diff()
    dfx['DeathsNew']        = dfx['Deaths'].diff()
    dfx['ConfirmedNewMean'] = dfx['ConfirmedNew'].rolling(7).mean()
    dfx['DeathsNewMean']    = dfx['DeathsNew'].rolling(7).mean()
    dfx                     = dfx.drop(dfx.index[[0,1,2,3,4,5,6]])
    #print(dfx.head(n=10))

    file_name = dfa['Country'].values[0] + '.csv'
    file_name = file_name.replace(',', '')
    file_name = file_name.replace('*', '')
    file_path = os.path.join(csvFolder, file_name)
    dfx.to_csv(file_path, index=False)

    index_entry = [dfKey, file_name, dfx['Lat'].values[0], dfx['Long'].values[0]]

    return index_entry

# ----------------------------------------------------------------------------
# Find keys for countries that have provinces and no overall country numbers
# ----------------------------------------------------------------------------

def find_other_keys(inKeys, df):
    keys = []
    count = 0
    last_country = ''
    
    for key in inKeys:
        words = key.split(' / ')
        if words[1] != '':
            if words[0] != last_country:
                keys.append(words[0])
                last_country = words[0]
                #print('Last country:', last_country, 'Province:', words[1])
        else:
            lastCountry = words[0]

        count += 1

    return keys

# ----------------------------------------------------------------------------
# Main line
# ----------------------------------------------------------------------------

def main():
    if testing == True:
        print('TESTING ----------------------------')
    df = prepare_dataframe()
    create_csvs(df)

if __name__ == '__main__':
    main()
