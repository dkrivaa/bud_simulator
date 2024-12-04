import streamlit as st

from functions.data import files_dict, available_budget_types, read_data
from functions.system import startup, budget_model


# Top level options - New simulation / upload simulation
def top_level():
    options = ['New Simulation', 'Upload Saved Simulation']
    selection = st.radio(label='Choose Option',
                         options=options,
                         index=None,
                         key='selection')
    if selection is not None:
        return options.index(selection)


# Selecting year of budget model
def year_selection():
    options = list(files_dict().keys())[:-1]
    year = st.radio(label='Year',
                    options=options,
                    index=None,
                    key='year')
    if year is not None:
        if year != 2024:
            return year
        else:
            return special_2024()


def special_2024():
    options = ['Before 7.10.2023', 'After 7.10.2023']
    special = st.radio(label='choose',
                       options=options,
                       index=None,
                       key='special')
    if special is not None:
        if options.index(special) == 0:
            return 20241
        else:
            return 2024


def budget_type(year):
    options = available_budget_types()[year]
    budget = st.radio(label='Budget',
                      options=options,
                      index=None,
                      key='budget')
    return budget


def new_simulation_button(year, budget_type):
    if st.button(label='Create New Simulation', key='new_simulation'):
        with st.spinner('Preparing system and reading data.....'):
            startup()
            budget_model(year, budget_type)
            read_data(year, budget_type)
        st.switch_page('views/simulation.py')


def upload_simulation_button():
    if st.button(label='Upload Simulation'):
        st.session_state.clear()
        st.switch_page('views/upload.py')


# Page
st.title('Budget Simulator')
st.divider()

selection = top_level()
if selection is not None:
    # If selection is 'New Simulation'
    if selection == 0:
        st.write(':orange[Define Base Budget Model (Starting point)]')
        year = year_selection()
        if year:
            budget_type = budget_type(year)
            if budget_type:
                new_simulation_button(year, budget_type)
    # If selection is 'Upload Simulation'
    if selection == 1:
        upload_simulation_button()
