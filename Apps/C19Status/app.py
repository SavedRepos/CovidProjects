#!/usr/bin/env python3
#
# app.py
#
# app.py is a web application written in Python and using
# Streamlit as the presentation method.
#

import datetime
from   datetime import timedelta
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd
import streamlit as st

import awesome_streamlit as ast
import constants as cn
import src.pages.about
import src.pages.bccases
import src.pages.countries
import src.pages.provinces
import src.pages.vaccinations

ast.core.services.other.set_logging_format()

PAGES = {
    "B.C. Cases": src.pages.bccases,
    "Vaccinations": src.pages.vaccinations,
    "Provinces": src.pages.provinces,
    "Countries": src.pages.countries,
    "About": src.pages.about,
}

# #######################################################################################
# Global Variables
# #######################################################################################

canada_url = f'{cn.CASES_BASE_URL}Canada.csv'
df = pd.read_csv(canada_url)

dfLast = df.tail(n=1)
cn.LAST_DATE = dfLast['Date'].values[0]

dfFirst = df.head(n=1)
cn.FIRST_DATE = dfFirst['Date'].values[0]

date_range = f'Data range: {cn.FIRST_DATE} to {cn.LAST_DATE}'

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
