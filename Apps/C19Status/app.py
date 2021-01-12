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
    "B.C.": src.pages.bc,
    "Countries": src.pages.countries,
    "Provinces": src.pages.provinces,
    "Vaccinations": src.pages.vaccinations,
    "About": src.pages.about,
}

# ############################################################################
# Entry Point
# ############################################################################

def main():
    """Main function of the App"""
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))

    page = PAGES[selection]

    with st.spinner(f"Loading {selection} ..."):
        ast.shared.components.write_page(page)
    st.sidebar.title("About")
    st.sidebar.info(
        """
        All data used in this app is provided by official sources:
        ### Data Sources
        1. Case data is from [CSSE at Johns Hopkins University COVID-19 Github repository]
        (https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data).
        2. British Columbia testing data for from the [BC Centre for Disease Control]
        (http://www.bccdc.ca/Health-Info-Site/Documents/BCCDC_COVID19_Dashboard_Lab_Information.csv)
        3. Canadian vaccination data is found in the [COVID-19 Canada Github repository]
        (https://github.com/ishaberry/Covid19Canada)
        """
    )


if __name__ == "__main__":
    main()
