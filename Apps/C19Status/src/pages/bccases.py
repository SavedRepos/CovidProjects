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
    st.title("British Columbia Covid Stats")
    casesByHA()

#
#  Display Cases by Health Authority
#
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

    unique_has = df.HA.unique()
    #print(f'uniques_has: {unique_has}')
    for unique_ha in unique_has:
        #print(f'unique_ha: {unique_ha}')
        dfha = df[df['HA'] == unique_ha]
        dfhagr =  pd.DataFrame(dfha.groupby(['HA', 'HSDA'], as_index=False).sum())
        ha = ''
        hsda = ''
        casex = ''
        casey = ''
        previous_ha = ''
        table_row = ''
        for index, row in dfhagr.iterrows():
            if row['HA'] != previous_ha:
                if previous_ha != '':
                    table_row = f'<tr valign="top"><td>{ha}</td><td>{hsda}</td><td style="text-align:right">{casex}</td><td style="text-align:right">{casey}</td></tr>\n'
                    table_rows += table_row
                    print('New' + table_row)
                ha = f"<b>{row['HA']}</b>"
                hsda = f"<b>{row['HSDA']}</b>"
                casex = f"<b>{'{:,}'.format(row['Cases_Reported_x'])}</b>"
                casey = f"<b>{'{:,}'.format(row['Cases_Reported_y'])}</b>"
                previous_ha = row['HA']
            else:
                hsda += f"<br />{row['HSDA']}"
                casex += f"<br />{'{:,}'.format(row['Cases_Reported_x'])}"
                casey += f"<br />{'{:,}'.format(row['Cases_Reported_y'])}"
        table_row = f'<tr valign="top"><td>{ha}</td><td>{hsda}</td><td style="text-align:right">{casex}</td><td style="text-align:right">{casey}</td></tr>\n'
        table_rows += table_row
        #print('Add', table_row)

    table_rows += '</table>\n'
    table_rows += '</div>\n'
    
    st.markdown('#### BCCDC Cases by Region')
    st.markdown('#### ')
    st.markdown(table_rows, unsafe_allow_html=True)
