import pandas as pd
import streamlit as st
import json

from functions.system import startup, budget_model
from functions.data import read_data
from functions.form_elements import possible_action_keys
from functions.budget import (change_quick_measures_action, change_wage_policies_action,
                              change_manpower_programs_action, change_other_programs_action)


# Initialize simulation
def initialize_simulation(year, budget_type):
    with st.spinner('Preparing system and reading data.....'):
        startup()
        budget_model(year, budget_type)
        read_data(year, budget_type)


# Check uploaded file
def check_file(df_actions):
    file_columns = df_actions.columns.tolist()
    possible_keys = possible_action_keys()
    if len(df_actions) > 0:
        return set(file_columns).issubset(set(possible_keys))
    else:
        return False


def read_csv(file):
    df_actions = pd.read_csv(file)

    # Safely Deserialize list columns
    def safe_json_loads(x):
        if pd.isna(x) or x == "" or not isinstance(x, str):
            return None
        try:
            return json.loads(x)
        except json.JSONDecodeError:
            return None

    # Deserialize list columns
    list_columns = ["takanot", "budget"]
    if set(list_columns).issubset(set(df_actions.columns.tolist())):
        for col in list_columns:
            df_actions[col] = df_actions[col].apply(safe_json_loads)

    return df_actions


# Add saved actions to simulation
def add_saved_actions(df_actions):
    for _, row in df_actions.iterrows():
        # Add action to session_state['actions']
        st.session_state['actions'].append(row.to_dict())
        # Update session_state['df']
        # If Quick Measures
        if row['action_type'] == 0:
            change_quick_measures_action(action_type=row['action_type'],
                                         action=row['action'],
                                         percent=row['percent'],
                                         action_status='add_action')

        # If Wage Policies
        elif row['action_type'] == 2:
            change_wage_policies_action(action_type=row['action_type'],
                                        action=row['action'],
                                        percent=row['percent'],
                                        action_status='add_action')

        # If Manpower program
        elif row['action_type'] == 1 and row['action'] != 2:
            change_manpower_programs_action(action_type=row['action_type'],
                                            action=row['action'],
                                            op_manpower=row['op_manpower'],
                                            admin_manpower=row['admin_manpower'],
                                            students=row['students'],
                                            action_status='add_action')

        # If Other Programs
        elif row['action_type'] == 1 and row['action'] == 2:
            change_other_programs_action(action_type=row['action_type'],
                                         takanot_list=row['takanot'],
                                         budget_list=row['budget'],
                                         action_status='add_action')


##########################
# Page
st.title('Upload Simulation')
st.divider()
file = st.file_uploader(label='Upload Saved Simulation File (csv)',
                        type='csv',)

if file:
    # if file
    df_actions = read_csv(file)
    # Checking the uploaded file.
    if check_file(df_actions):
        year = df_actions['year'].unique().tolist()[0]
        budget_type = df_actions['budget_type'].unique().tolist()[0]
        # Initializing simulation - session_state and reading budget data
        if st.button(label='Create New Simulation', key='new_simulation'):
            initialize_simulation(year, budget_type)

        # Add saved actions to simulation
        if 'df' in st.session_state:
            add_saved_actions(df_actions)

            st.switch_page('views/simulation.py')

    # If file has no data or column names do not confirm to possible keys
    else:
        # Create a placeholder for the "modal"
        placeholder = st.empty()

        with placeholder.container():
            st.error("The file does not confirm to system demands")
            if st.button("Back"):
                placeholder.empty()  # Close the "modal"
                st.switch_page("views/start.py")

        # Prevent other UI interactions by not rendering additional elements
        st.stop()





