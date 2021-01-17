#!/usr/bin/env python3
#
# provinces.py
#
# provinces.py is part of a web application written in Python and using
# Streamlit as the presentation method.
#

"""bccases page shows Canadian Provinces Cases"""
import datetime
from datetime import timedelta
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
    st.title("Vaccinations by Day")
    st.markdown('#### ')

# Canada Vaccination stats
# "date_vaccine_administered","province","cumulative_avaccine"
# CANADA_VACCINATION_ADMINSTERED = 'https://raw.githubusercontent.com/ccodwg/Covid19Canada/master/vaccine_administration_cumulative.csv'
# "date_vaccine_distributed","province","cumulative_dvaccine"
# CANADA_VACCINATION_DISTRIBUTED = 'https://raw.githubusercontent.com/ccodwg/Covid19Canada/master/vaccine_distribution_cumulative.csv'

    dfAdmin = pd.read_csv(cn.CANADA_VACCINATION_ADMINSTERED)
    dfAdmin = dfAdmin.sort_values(['date_vaccine_administered'], ascending=[True])
    dfAdmin['cumulative_avaccine_mean'] = dfAdmin['cumulative_avaccine'].rolling(7).mean()
    print(dfAdmin)

    dfDistr = pd.read_csv(cn.CANADA_VACCINATION_DISTRIBUTED)
    dfDistr = dfDistr.sort_values(['date_vaccine_distributed'], ascending=[True])
    dfDistr['cumulative_dvaccine_mean'] = dfDistr['cumulative_dvaccine'].rolling(7).mean()
    print(dfDistr)

