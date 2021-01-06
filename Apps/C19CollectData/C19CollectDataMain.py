#!/usr/bin/env python3
#
# CovidDataMain.py
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

import C19CollectDataGlobalTimeSeries as gts
import C19CollectDataGlobalRollup as gpr
import C19CollectDataUSStates as uss
import C19CollectDataWriteCsv as wcs

# ----------------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------------

CSV_DIRECTORY    = '/Users/paulhart/Development/CovidProjects/Data/CSV_Files'

CONFIRMED_GLOBAL = '/Users/paulhart/Development/CovidProjects/Data/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
CONFIRMED_US     = '/Users/paulhart/Development/CovidProjects/Data/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv'
DEATHS_GLOBAL    = '/Users/paulhart/Development/CovidProjects/Data/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
DEATHS_US        = '/Users/paulhart/Development/CovidProjects/Data/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv'

WORLD_POP        = '/Users/paulhart/Development/CovidProjects/Data/WorldPop.csv'

# ----------------------------------------------------------------------------
# Global Variables
# ----------------------------------------------------------------------------

global global_keys
global global_new_keys
#global file_index_entry
#global file_index

class file_index_entry():
    combined_key = ''
    file_name = ''
    country = ''
    province = ''

    def __init__(self, combined_key, file_name, country, province):
        self.combined_key = combined_key
        self.file_name = file_name
        self.country = country
        self.province = province

file_index = []

dfPopulations = pd.read_csv(WORLD_POP)

# ----------------------------------------------------------------------------
# Prepare dataframe
# ----------------------------------------------------------------------------

def process_dataframe():
    ''' Processing global and US state data'''

    dfGlobal = gts.processGlobalDataframe()
    gpr.processProvinceRollup(dfGlobal)
    uss.processUSDataframe()
    wcs.writeWriteIndexCsv()

# ----------------------------------------------------------------------------
# Entry point
# ----------------------------------------------------------------------------

def main():
    df = process_dataframe()

if __name__ == '__main__':
    main()
