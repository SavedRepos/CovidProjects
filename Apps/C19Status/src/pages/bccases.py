#!/usr/bin/env python3
#
# bccases.py
#
# bccases.py is part of a web application written in Python and using
# Streamlit as the presentation method.
#

"""bccases page shows BC Covid Cases"""
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
    st.title("BC Covid Cases")

    prov = 'British Columbia'
    
    file_name = f'{prov}.csv'.replace(' ', '%20')
    dfProv = pd.read_csv(f'{cn.CASES_BASE_URL}{file_name}')
    
    dfTests = pd.read_csv(cn.BC_TESTS_URL)
    dfTable = dfTests.copy() 
    dfTable['New_Positives'] = dfTable['New_Tests'] * (dfTable['Positivity'] / 100)

    dfTable = dfTable.groupby('Date').agg({'New_Tests': 'sum', 'New_Positives': 'sum', 'Positivity': 'mean', 'Turn_Around': 'mean'})
    dfTable = dfTable.sort_values('Date', ascending=False)
    dfTable = pd.merge(dfProv, dfTable, on=['Date'], how='outer')
    dfTable = dfTable.replace(np.nan,0)

    st.markdown('<hr style="border-top: 8px solid #ccc; border-radius: 5px;" />', unsafe_allow_html=True)
    casesByDate(dfTable)
    st.markdown('<hr style="border-top: 8px solid #bbb; border-radius: 5px;" />', unsafe_allow_html=True)
    graphsByGraphs(dfProv)
    st.markdown('<hr style="border-top: 8px solid #bbb; border-radius: 5px;" />', unsafe_allow_html=True)
    casesByHA()

#
#  Display Cases by date
#
def casesByDate(dfProv):
    st.markdown('#### BC New Cases and Deaths by Date')
    st.markdown('#### ')
    
    #st.markdown(f'##### 10 Days')

    # Table of details for last week 
    cases_data = '<div style="font-size: 9pt">\n'
    cases_data += '<table border=1>\n'
    cases_data += '<tr><th> </th><th colspan=2 style="text-align:center">Cases</th><th colspan=2 style="text-align:center">Deaths</th><th colspan=4 style="text-align:center">Testing</th></tr>\n'
    cases_data += '<tr><th>Date</th><th>Total</th><th>New</th><th>Total</th><th>New</th><th>New</th><th>Positives</th><th>% Pos.</th><th>Hours</th></tr>\n'
    #cases_data += '| :----- | ----------: | --------: | -----------: | ---------: |\n'
    row_count = 0
    dfSorted = dfProv.sort_values(['Date'], ascending=False)
    for index, row in dfSorted.iterrows():
        date = row['Date'] 
        confirmed = row['Confirmed']
        confirmed = "{:,}".format(confirmed)
        confirmedNew = row['ConfirmedNew']
        confirmedNew = "{:,}".format(confirmedNew)
        deaths = row['Deaths']
        deaths = "{:,}".format(deaths)
        deathsNew = row['DeathsNew']
        deathsNew = "{:,}".format(deathsNew)
        #New_Tests  New_Positives  Positivity  Turn_Around
        newTests = row['New_Tests']
        newTests = "{:,.0f}".format(newTests)
        newPositives = row['New_Positives']
        newPositives = "{:,.0f}".format(newPositives)
        positivity = row['Positivity']
        positivity = "{:.1f}".format(positivity)
        turnAround = row['Turn_Around']
        turnAround = "{:.1f}".format(turnAround)
        cases_data += f'<tr>'
        cases_data += f'<td nowrap>{date}</td><td style="text-align:right">{confirmed}</td>'
        cases_data += f'<td style="text-align:right">{confirmedNew}</td>'
        cases_data += f'<td style="text-align:right">{deaths}</td>'
        cases_data += f'<td style="text-align:right">{deathsNew}</td>'
        cases_data += f'<td style="text-align:right">{newTests}</td>'
        cases_data += f'<td style="text-align:right">{newPositives}</td>'
        cases_data += f'<td style="text-align:right">{positivity}%</td>'
        cases_data += f'<td style="text-align:right">{turnAround}</td>'
        cases_data += f'</tr>' + '\n'
        row_count += 1
        if row_count >= 10:
            cases_data += '</table>\n'
            cases_data += '</div>\n'
            break
    st.markdown(cases_data, unsafe_allow_html=True)

#
#  Display Cases on a graph
#
def graphsByGraphs(dfProv):    
    st.markdown('#### BC New Cases and Deaths by Date')
    st.markdown('#### ')

    #-------------------------------------------------------------------------
    # Create Confirmed New Plot
    #-------------------------------------------------------------------------
    col1, col2 = st.beta_columns(2)
    with col1:

        #st.markdown(f'##### New Cases')

        fig1 = plt.figure(1, figsize=(8, 5))

        plt.title('New Cases - Smoothed', fontsize='large')
        plt.xlabel="Date"
        plt.ylabel="Number"

        #plt.xticks(rotation=45)
        ax = plt.gca()
        ax.xaxis.set_major_locator(ticker.MultipleLocator(100))

        plt.plot(dfProv['Date'], dfProv['ConfirmedNewMean'], label='New Cases - Smoothed')
        plt.grid(b=True, which='major')
        
        st.pyplot(fig1)
        plt.close()

    #-------------------------------------------------------------------------
    # Create Deaths New Plot
    #-------------------------------------------------------------------------

    with col2:
        
        fig2 = plt.figure(2, figsize=(8, 5))

        plt.title('New Deaths - Smoothed')
        plt.xlabel="Date"
        plt.ylabel="Number"

        #plt.xticks(rotation=45)
        ax = plt.gca()
        ax.xaxis.set_major_locator(ticker.MultipleLocator(100))

        plt.plot(dfProv['Date'], dfProv['DeathsNewMean'], label='New Deaths - Smoothed')
        plt.grid(b=True, which='major')
        st.pyplot(fig2)
        plt.close()

#
#  Display Cases by Health Authority
#
def casesByHA():

    # Create dataframe with all records
    df = pd.read_csv(cn.BC_REGIONAL_URL)
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
    table_rows += '<tr><th>Health Authority</th><th>Heath Services Delivery Area</th><th colspan=4 style="text-align:center">Cases</th></tr>\n'
    table_rows += '<tr><th></th><th></th><th colspan=2>Last 7 Days</th><th colspan=2>Cases Total</th></tr>\n'

    unique_has = df.HA.unique()
    for unique_ha in unique_has:
        dfha = df[df['HA'] == unique_ha]
        dfhagr =  pd.DataFrame(dfha.groupby(['HA', 'HSDA'], as_index=False).sum())
        ha = ''
        hsda = ''
        casex = ''
        casey = ''
        casex_total = 0
        casey_total = 0
        casex_percent = 0
        casey_persent = 0

        previous_ha = ''
        table_row = ''
        casex_total = ''
        casey_total = ''
        casex_percent = ''
        casey_percent = ''
        for index, row in dfhagr.iterrows():
            if row['HA'] != previous_ha:
                if previous_ha != '':
                    table_row = f'<tr valign="top"><td>{ha}</td><td>{hsda}</td><td style="text-align:right">{casex}</td><td style="text-align:right">{casey}</td></tr>\n'
                    table_rows += table_row
                ha = f"<b>{row['HA']}</b>"
                hsda = f"<b>{row['HSDA']}</b>"
                casex = f"<b>{'{:,}'.format(row['Cases_Reported_x'])}</b>"
                casey = f"<b>{'{:,}'.format(row['Cases_Reported_y'])}</b>"
                casex_total = row['Cases_Reported_x']
                casey_total = row['Cases_Reported_y']
                casex_percent = '<b>100.00%</b>'
                casey_percent = '<b>100.00%</b>'
                previous_ha = row['HA']
            else:
                hsda += f"<br />{row['HSDA']}"
                casex += f"<br />{'{:,}'.format(row['Cases_Reported_x'])}"
                casey += f"<br />{'{:,}'.format(row['Cases_Reported_y'])}"
                casex_percent += f"<br />" + '{:.2f}'.format((row['Cases_Reported_x'] /  casex_total) * 100) + '%'
                casey_percent += f"<br />" + '{:.2f}'.format((row['Cases_Reported_y'] /  casey_total) * 100) + '%'
        table_row = f'<tr valign="top"><td>{ha}</td><td>{hsda}</td><td style="text-align:right">{casex}</td><td style="text-align:right">{casex_percent}</td><td style="text-align:right">{casey}</td><td style="text-align:right">{casey_percent}</td></tr>\n'
        table_rows += table_row

    table_rows += '</table>\n'
    table_rows += '</div>\n'
    
    st.markdown('#### BCCDC Cases by Health Authority')
    st.markdown('#### ')
    st.markdown(table_rows, unsafe_allow_html=True)
