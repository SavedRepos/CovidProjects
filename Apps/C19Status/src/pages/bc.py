#!/usr/bin/env python3
#
# bc.py
#
# bc.py is a web application written in Python and using
# Streamlit as the presentation method.
#

"""BC page shows BC Covid stats"""
import datetime
from datetime import timedelta
import pandas as pd
import streamlit as st
import awesome_streamlit as ast

import app 

# pylint: disable=line-too-long
def write():
    """Used to write the page in the app.py file"""
    with st.spinner("Loading Home ..."):
        #ast.shared.components.title_awesome("and so it goes...")
        st.title("British Columbia Covid Stats")
    casesByHA()


def casesByHA():

    # Create dataframe with all records
    df = pd.read_csv(app.BC_REGIONAL_URL)
    df = df.drop(columns=['Cases_Reported_Smoothed'])
    df = df.sort_values(by=['Date', 'HA', 'HSDA'], ascending=[False, True, True])

    # Create dataframe with records fromlast 7 days
    last_date = df.Date.values[0]
    first_date = (datetime.datetime.strptime(last_date, '%Y-%m-%d') - timedelta(days = 7)).strftime('%Y-%m-%d')
    dfw = df[df['Date'] > first_date]

    # Group by HA and HSDA
    dfg = pd.DataFrame(df.groupby(['HA', 'HSDA'], as_index=False).sum())
    dfw = pd.DataFrame(dfw.groupby(['HA', 'HSDA'], as_index=False).sum())

    # Merge into a single dataframe
    df  = dfw.merge(dfg, left_on=['HA','HSDA'], right_on=['HA','HSDA'])

    # Table of details for last week 
    table_rows =  '<div style="font-size: 9pt">\n'

    table_rows += '<table border=1 cellspacing=0 cellpadding=0>\n'
    table_rows += '<tr><th>Health Authority</th><th>Heath Services Delivery Area</th><th colspan=2 style="text-align:center">Cases</th></tr>\n'
    table_rows += '<tr><th></th><th></th><th>Last 7 Days</th><th>Cases Total</th></tr>\n'

    last_ha = ''
    for index, row in df.iterrows():
        ha = row['HA']
        if ha == last_ha:
            ha = ''
        else:
            #ha = f'<b>{ha}</b>'
            last_ha = ha
        if ha == 'All':
            ha = 'Total'
        hsda = row['HSDA']
        if hsda == 'All':
            hsda = 'Total'
        casesX = "{:,}".format(row['Cases_Reported_x'])
        casesY = "{:,}".format(row['Cases_Reported_y'])
        table_row = f'<tr><td cellspacing=1 cellpadding=1>{ha}</td><td cellspacing=1 cellpadding=1>{hsda}</td><td style="text-align:right">{casesX}</td><td style="text-align:right" cellspacing=1 cellpadding=1>{casesY}</td></tr>\n'
        table_rows += table_row

    table_rows += '</table>\n'
    table_rows += '</div>\n'
    
    st.markdown('#### BCCDC Cases by Region')
    st.markdown(table_rows, unsafe_allow_html=True)
