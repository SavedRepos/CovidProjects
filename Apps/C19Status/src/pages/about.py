#!/usr/bin/env python3
#
# about.py
#
# app.py is a web application written in Python and using
# Streamlit as the presentation method.
#

"""About page shown when the user enters the application"""
import streamlit as st
import awesome_streamlit as ast

# pylint: disable=line-too-long
def write():
    """Used to write the page in the app.py file"""
    with st.spinner("Loading About ..."):
        st.title("Covid-19 in British Columbia - About")
        st.markdown(
            """## Background

This project was developed in order to scratch several itches. One of those itches is the result of the boredom attendant 
with being locked down and an interest in the progress of outbreak. 

The project is hosted at 'github.com' and can be found at 
[https://github.com/jpaulhart/CovidData](https://github.com/jpaulhart/CovidData) 

## The Developer

This project is developed by Paul Hart. He is desperately trying to to disprove the old adage 
'*you can't teach an old dog new tricks*'
""",
            unsafe_allow_html=True,
        )

