#!/usr/bin/env python3
#
# C19CollectDataWriteCsv
#
# Prepare the data from Github and produce the csv files for other apps
#

import csv
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

def writeWriteIndexCsv():

    index_file_name = cd.CSV_DIRECTORY + '/Index.csv'

    with open(index_file_name, mode='w') as index_csv_file:
        index_csv_writer = csv.writer(index_csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        index_csv_writer.writerow(['combined_key', 'file_name', 'country', 'province'])    
        for entry in cd.file_index:
            index_csv_writer.writerow([entry.combined_key, entry.file_name, entry.country, entry.province])