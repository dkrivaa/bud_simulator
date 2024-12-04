import streamlit as st
import pandas as pd


from functions.system import initial_check
from functions.form_elements import action_types, action_summary


# Check that simulation has been initialized else go back to start page
initial_check()

with st.container():
    st.title('Actions Summary')
    st.page_link(page='views/simulation.py', label='Back to Simulator')
    st.divider()
    # Summary of all actions
    tab1, tab2, tab3 = st.tabs(action_types())

    with tab1:
        action_summary(action_type=0)
    with tab2:
        action_summary(action_type=1)
    with tab3:
        action_summary(action_type=2)





