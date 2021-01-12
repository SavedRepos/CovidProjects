#!/usr/bin/env python3
#
# bc.py
#
# bc.py is a web application written in Python and using
# Streamlit as the presentation method.
#

"""BC page shows BC Covid stats"""
import streamlit as st

import awesome_streamlit as ast


# pylint: disable=line-too-long
def write():
    """Used to write the page in the app.py file"""
    with st.spinner("Loading Home ..."):
        #ast.shared.components.title_awesome("and so it goes...")
        st.title("British Columbia Covid Stats")
        with st.beta_expander("Confirmed Cases and Deaths", expanded=True):
            st.write("""
                The chart above shows some numbers I picked for you.
                I rolled actual dice for these, so they're *guaranteed* to
                be random.
            """)
        with st.beta_expander("Confirmed Cases by Health Authority", expanded=False):
            st.write("""
                The chart above shows some numbers I picked for you.
                I rolled actual dice for these, so they're *guaranteed* to
                be random.
            """)
