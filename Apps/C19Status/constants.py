#!/usr/bin/env python3
#
# constants.py
#
# app.py is a web application written in Python and using
# Streamlit as the presentation method.
#

# #######################################################################################
# Global Constants
# #######################################################################################

# Country files base url
# Field Names:
# Province_State, Country_Region, Lat, Long, Date, Confirmed, Deaths, Combined_Key, Population,
# ConfirmedNew, DeathsNew, ConfirmedNewMean, DeathsNewMean
# Country.csv fields
CASES_BASE_URL = 'https://raw.githubusercontent.com/jpaulhart/CovidProjects/main/Data/CSV_Files/'

# BC CDC testing data locations
# Field Names:
# "Date", "Region", "New_Tests", "Total_Tests", "Positivity", "Turn_Around"
BC_TESTS_URL = 'http://www.bccdc.ca/Health-Info-Site/Documents/BCCDC_COVID19_Dashboard_Lab_Information.csv'
# "Reported_Date","HA","Sex","Age_Group","Classification_Reported"
BC_CASES_URL = 'http://www.bccdc.ca/Health-Info-Site/Documents/BCCDC_COVID19_Dashboard_Case_Details.csv'
# "Date","Province","HA","HSDA","Cases_Reported","Cases_Reported_Smoothed"
BC_REGIONAL_URL = 'http://www.bccdc.ca/Health-Info-Site/Documents/BCCDC_COVID19_Regional_Summary_Data.csv'

# combined_key,file_name,country,province
# Index.csv fields

# Provincial Population
PROV_POP = {
    'BC' : 5.071,
    'AL' : 4.371,
    'SA' : 1.174,
    'MB' : 1.369,
    'ON' : 14.57,
    'PQ' : 8.485,
    'NL' : 0.552,
    'NB' : 0.777,
    'NS' : 0.971,
    'PE' : 0.156,
}

FIRST_DATE = ""
LAST_DATE = ""
