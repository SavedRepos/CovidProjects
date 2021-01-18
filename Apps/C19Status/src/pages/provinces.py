#!/usr/bin/env python3
#
# provinces.py
#
# provinces.py is part of a web application written in Python and using
# Streamlit as the presentation method.
#

"""bccases page shows Canadian Provinces Cases"""
import datetime
from   datetime import timedelta
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd
import streamlit as st
import awesome_streamlit as ast

import constants as cn

# pylint: disable=line-too-long
def write():
    """Used to write the page in the app.py file"""
    st.title("Canadian Provinces Covid Cases")
    st.markdown('#### ')

    st.markdown('----')
    st.markdown(f"#### Compare Canada's Largest Provinces")

    dfal = pd.read_csv(f'{cn.CASES_BASE_URL}Alberta.csv')
    #dfal = df_days(dfal, last_date, time_frame)
    dfal['ConfirmedNewPer1M'] = dfal['ConfirmedNewMean'] / cn.PROV_POP['AL']
    dfal['DeathsNewPer1M']    = dfal['DeathsNewMean'] / cn.PROV_POP['AL']

    dfbc = pd.read_csv(f'{cn.CASES_BASE_URL}British%20Columbia.csv')
    #dfbc = df_days(dfbc, last_date, time_frame)
    dfbc['ConfirmedNewPer1M'] = dfbc['ConfirmedNewMean'] / cn.PROV_POP['AL']
    dfbc['DeathsNewPer1M']    = dfbc['DeathsNewMean'] / cn.PROV_POP['AL']

    dfon = pd.read_csv(f'{cn.CASES_BASE_URL}Ontario.csv')
    #dfon = df_days(dfon, last_date, time_frame)
    dfon['ConfirmedNewPer1M'] = dfon['ConfirmedNewMean'] / cn.PROV_POP['AL']
    dfon['DeathsNewPer1M']    = dfon['DeathsNewMean'] / cn.PROV_POP['AL']

    dfqu = pd.read_csv(f'{cn.CASES_BASE_URL}Quebec.csv')
    #dfqu = df_days(dfqu, last_date, time_frame)
    dfqu['ConfirmedNewPer1M'] = dfqu['ConfirmedNewMean'] / cn.PROV_POP['AL']
    dfqu['DeathsNewPer1M']    = dfqu['DeathsNewMean'] / cn.PROV_POP['AL']

    col1, col2 = st.beta_columns(2)

    #-------------------------------------------------------------------------
    # Create Confirmed New Plot
    #-------------------------------------------------------------------------

    #with col1:

    #st.markdown(f'##### New Cases')

    fig1 = plt.figure(1, figsize=(8, 5))

    plt.title('Confirmed New Cases per Million', fontsize='large')
    plt.xlabel="Date"
    plt.ylabel="Number"

    #plt.xticks(rotation=45)
    ax = plt.gca()
    ax.xaxis.set_major_locator(ticker.MultipleLocator(75))

    #plt.plot(dfPr['date'], dfProv['confirmedNewMean'], label='New Cases - Smoothed')
    plt.plot(dfal['Date'], dfal['ConfirmedNewPer1M'], label='Alberta')
    plt.plot(dfbc['Date'], dfbc['ConfirmedNewPer1M'], label='British Columbia')
    plt.plot(dfon['Date'], dfon['ConfirmedNewPer1M'], label='Ontario')
    plt.plot(dfqu['Date'], dfqu['ConfirmedNewPer1M'], label='Quebec')

    # Add a legend
    plt.legend(['Alberta', 'British Columbia', 'Ontario', 'Quebec'])
    plt.grid(b=True, which='major')
    st.pyplot(fig1)
    plt.close()

    #-------------------------------------------------------------------------
    # Create Deaths New Plot
    #-------------------------------------------------------------------------

    #with col2:

    #st.markdown(f'##### New Deaths')

    fig1 = plt.figure(1, figsize=(8, 5))

    plt.title('New Deaths per Million', fontsize='large')
    plt.xlabel="Date"
    plt.ylabel="Number"

    #plt.xticks(rotation=45)
    ax = plt.gca()
    ax.xaxis.set_major_locator(ticker.MultipleLocator(75))

    #plt.plot(dfPr['date'], dfProv['confirmedNewMean'], label='New Cases - Smoothed')
    plt.plot(dfal['Date'], dfal['DeathsNewPer1M'], label='Alberta')
    plt.plot(dfbc['Date'], dfbc['DeathsNewPer1M'], label='British Columbia')
    plt.plot(dfon['Date'], dfon['DeathsNewPer1M'], label='Ontario')
    plt.plot(dfqu['Date'], dfqu['DeathsNewPer1M'], label='Quebec')

    # Add a legend
    plt.legend(['Alberta', 'British Columbia', 'Ontario', 'Quebec'])
    plt.grid(b=True, which='major')
    st.pyplot(fig1)
    plt.close()
