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

# ----------------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------------

CSV_DIRECTORY    = '/Users/paulhart/CovidProjects/Data/CSV_Files'

CONFIRMED_GLOBAL = '/Users/paulhart/CovidProjects/Data/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
CONFIRMED_US     = '/Users/paulhart/CovidProjects/Data/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv'
DEATHS_GLOBAL    = '/Users/paulhart/CovidProjects/Data/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
DEATHS_US        = '/Users/paulhart/CovidProjects/Data/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv'

WORLD_POP        = '/Users/paulhart/CovidProjects/Data/WorldPop.csv'

# ----------------------------------------------------------------------------
# Global Variables
# ----------------------------------------------------------------------------

global global_keys
global global_new_keys

dfPopulations = pd.read_csv(WORLD_POP)

# ----------------------------------------------------------------------------
# Prepare dataframe
# ----------------------------------------------------------------------------

def process_dataframe():
    ''' Processing global and US state data'''

    dfGlobal = gts.processGlobalDataframe()
    dfGlobal = gpr.processProvinceRollup(dfGlobal)

    dfUS = uss.processUSDataframe()


# ----------------------------------------------------------------------------
# Entry point
# ----------------------------------------------------------------------------

def main():
    df = process_dataframe()

if __name__ == '__main__':
    main()
