"""
This program is aimed at making new Fire Authority budget in a simple and easy way,
based on a previous budget selected by user.
After selecting a budget model, the user can use a number of ways to construct a new budget
by taking advantage of the various build-in functions.
"""

import streamlit as st


start_page = st.Page(
    page='views/start.py',
    title='Start',
    default=True
)

simulation_page = st.Page(
    page='views/simulation.py',
    title='Simulator'
)

upload_page = st.Page(
    page='views/upload.py',
    title='Upload Simulation'
)

save_page = st.Page(
    page='views/save.py',
    title='Save / Download'
)

quick_measures_page = st.Page(
    page='views/actions/quick_measures.py',
    title='Quick Measures'
)

programs_page = st.Page(
    page='views/actions/programs.py',
    title='Programs'
)

wage_policies_page = st.Page(
    page='views/actions/wage_policies.py',
    title='Wage Policies'
)

budget_page = st.Page(
    page='views/budget.py',
    title='Compare Budgets'
)

summary_page = st.Page(
    page='views/actions/summary.py',
    title='Actions Summary'
)


pages = {
  'Main': [start_page, simulation_page, upload_page],
  'Actions': [quick_measures_page, programs_page, wage_policies_page, summary_page],
   'Compare Budgets': [budget_page],
  'Save / Download': [save_page, ]
}


pg = st.navigation(pages=pages)

pg.run()
