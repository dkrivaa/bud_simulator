import streamlit as st
import pandas as pd

from functions.system import initial_check, check_actions
from functions.budget import list_of_takanot


def compare_budgets(compare):
    var_dict = {
        'Budget': 'הוצאה נטו',
        'Manpower': 'שיא כח אדם',
        'Amount': 'כמות'
    }
    var = var_dict[compare]
    df_original = st.session_state['original_df'].copy()
    df = st.session_state['df'].copy()
    df_compare = pd.merge(df_original[['קוד תקנה', var]].rename(columns={var: 'Original Budget'}),
                          df[['קוד תקנה', var]].rename(columns={'var': 'Simulation Budget'}),
                          on=['קוד תקנה'], how='outer')
    df_compare = df_compare[(df_compare['original_budget'].notna()) |
                            (df_compare['original_budget'] != 0) |
                            (df_compare['simulation_budget'].notna()) |
                            (df_compare['simulation_budget'] != 0)]

    for _, row in df_compare.iterrows():
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(row['קוד תקנה'])
        with col2:
            st.write(row['Original Budget'])
        with col3:
            st.write(row['Simulation Budget'])






# Check that simulation has been initialized else go back to start page
initial_check()
# # Check that there are actions
check_actions()


st.title('Compare Budgets')
st.page_link(page='views/simulation.py', label='Back to Simulator')
st.divider()

options = ['Budget', 'Manpower', 'Other Amounts']
tab1, tab2, tab3 = st.tabs(options)
with tab1:
    compare_budgets('Budget')
with tab2:
    compare_budgets('Manpower')
with tab3:
    compare_budgets('Amount')

