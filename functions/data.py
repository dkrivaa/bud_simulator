import streamlit as st
import pandas as pd


# Dict of available data files
def files_dict():
    # These files are downloaded from 'https://www.gov.il/he/departments/policies/tableau'
    return {
        2022: 'data_files/tableau_BudgetData2022.xlsx',
        2023: 'data_files/tableau_BudgetData2023.xlsx',
        2024: 'data_files/tableau_BudgetData2024.xls',
        20241: 'data_files/before0710original2024.xlsx',
    }


# Budget types
def budget_types():
    return {
        'Original': 'מקורי',
        'Approved': 'מאושר',
        'Executed': 'ביצוע'
    }


def available_budget_types():
    return {
        2022: ['Original', 'Approved', 'Executed'],
        2023: ['Original', 'Approved', 'Executed'],
        2024: ['Original', ],
        20241: ['Original', ],
    }


def fire_budget_codes():
    return {
        'קוד רמה 1': 1,
        'קוד רמה 2': 12,
        'קוד סעיף': 7,
        'קוד תחום': 760
    }


# Reading relevant user selected file and saving df to session_state
def read_data(year, budget_type):
    # Get relevant file
    file = files_dict()[year]
    # Reading whole file
    df = pd.read_excel(file)
    # Keep only fire authority data and relevant budget type
    keys = list(fire_budget_codes().keys())
    values = list(fire_budget_codes().values())
    df = df.loc[(df[keys[0]] == values[0]) &
                (df[keys[1]] == values[1]) &
                (df[keys[2]] == values[2]) &
                (df[keys[3]] == values[3]) &
                (df['סוג תקציב'] == budget_types()[budget_type])]
    # saving df to session_state
    st.session_state['df_original'] = df.copy()
    st.session_state['df'] = df


