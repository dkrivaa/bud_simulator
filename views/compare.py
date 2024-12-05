import streamlit as st

from functions.system import initial_check, check_actions


# Check that simulation has been initialized else go back to start page
initial_check()
# # Check that there are actions
check_actions()


st.title('Compare Budgets')
st.page_link(page='views/simulation.py', label='Back to Simulator')
st.divider()

options = ['Budget', 'Manpower', 'Other Amounts']
tab1, tab2, tab3 = st.tabs([options])

