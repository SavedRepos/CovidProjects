#!/usr/bin/env python3
#
# app.py
#
# app.py is a web application written in Python and using
# Streamlit as the presentation method.
#

import datetime
from datetime import timedelta
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd
import streamlit as st
import awesome_streamlit as ast

import src.pages.about
import src.pages.bc
import src.pages.countries
import src.pages.provinces
import src.pages.testing
import src.pages.vaccinations

# #######################################################################################
# Global Constants
# #######################################################################################

# "Date", "Region", "New_Tests", "Total_Tests", "Positivity", "Turn_Around"
BC_TESTS_URL = 'http://www.bccdc.ca/Health-Info-Site/Documents/BCCDC_COVID19_Dashboard_Lab_Information.csv'
# "Reported_Date","HA","Sex","Age_Group","Classification_Reported"
BC_CASES_URL = 'http://www.bccdc.ca/Health-Info-Site/Documents/BCCDC_COVID19_Dashboard_Case_Details.csv'
# "Date","Province","HA","HSDA","Cases_Reported","Cases_Reported_Smoothed"
BC_REGIONAL_URL = 'http://www.bccdc.ca/Health-Info-Site/Documents/BCCDC_COVID19_Regional_Summary_Data.csv'

# combined_key,file_name,country,province
# Index.csv fields

# Province_State, Country_Region, Lat, Long, Date, Confirmed, Deaths, Combined_Key, Population,
# ConfirmedNew, DeathsNew, ConfirmedNewMean, DeathsNewMean
# Country.csv fields

BASE_URL = 'https://raw.githubusercontent.com/jpaulhart/CovidProjects/main/Data/CSV_Files/'

# #######################################################################################
# Global Variables
# #######################################################################################

ast.core.services.other.set_logging_format()

PAGES = {
    "B.C. Cases": src.pages.bc,
    "B.C. Testing": src.pages.testing,
    "B.C. Vaccinations": src.pages.vaccinations,
    "Countries": src.pages.countries,
    "Provinces": src.pages.provinces,
    "About": src.pages.about,
}

last_date = ""
first_date = ""

canada_url = f'{BASE_URL}Canada.csv'
df = pd.read_csv(canada_url)

dfLast = df.tail(n=1)
last_date = dfLast['Date'].values[0]

dfFirst = df.head(n=1)
first_date = dfFirst['Date'].values[0]

date_range = f'Data date range: {first_date} to {last_date}'

# ############################################################################
# Entry Point
# ############################################################################

def main():
    """Main function of the App"""
    st.sidebar.subheader("COVID-19")
    st.sidebar.markdown(f'<div style="font-size: 9pt">{date_range}</div>\n', unsafe_allow_html=True)

    st.sidebar.subheader("Navigation")
    selection = st.sidebar.radio("Select report to view:", list(PAGES.keys()))

    page = PAGES[selection]

    with st.spinner(f"Loading {selection} ..."):
        ast.shared.components.write_page(page)
    st.sidebar.subheader("About")
    st.sidebar.info(
        """
        All data used in this app is provided by official sources:
        ### Data Sources
        1. Case data is from [CSSE at Johns Hopkins University COVID-19 Github repository]
        (https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data).
        2. BC testing data for from the [BC Centre for Disease Control]
        (http://www.bccdc.ca/Health-Info-Site/Documents/BCCDC_COVID19_Dashboard_Lab_Information.csv)
        3. Canadian vaccination data is found in the [COVID-19 Canada Github repository]
        (https://github.com/ishaberry/Covid19Canada)
        """
    )


if __name__ == "__main__":
    main()
