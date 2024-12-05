import streamlit as st
import pandas as pd

from functions.system import initial_check, check_actions
from functions.budget import list_of_takanot


def compare_budgets(compare):
    var_dict = {
        'budget': 'הוצאה נטו',
        'manpower': 'שיא כח אדם',
        'amount': 'כמות'
    }
    var = var_dict[compare]
    df_original = st.session_state['df_original'].copy()
    df = st.session_state['df'].copy()
    df_compare = pd.merge(df_original[['קוד ושם תקנה', var]].rename(columns={var: 'Original Budget'}),
                          df[['קוד ושם תקנה', var]].rename(columns={var: 'Simulation Budget'}),
                          on=['קוד ושם תקנה'], how='outer')
    df_compare = df_compare[(df_compare['Original Budget'] != 0) &
                            (df_compare['Simulation Budget'] != 0)]

    for _, row in df_compare.iterrows():

        st.write(row['קוד ושם תקנה'])
        st.write(f'Base Budget: {row['Original Budget']:,.0f}')
        st.write(f'Simulation: {row['Simulation Budget']:,.0f}')
        st.divider()






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
    compare_budgets('budget')
with tab2:
    compare_budgets('manpower')
with tab3:
    compare_budgets('amount')

