import pandas as pd
import streamlit as st

from functions.system import initial_check, apply_action
from functions.form_elements import (action_selection, action_name, add_manpower, budget_impact,
                                     manpower_impact, investments, check_action_name, select_takana,
                                     program_dataframe, add_budget, display_with_delete)
from functions.budget import total_budget, total_manpower, manpower_program, other_programs


# Check that simulation has been initialized else go back to start page
initial_check()


#################################################
# PAGE
with st.container():
    st.title(':blue[Actions] - Programs')
    st.divider()
    action = action_selection(action_type=1)
    st.divider()

    # Manpower programs
    if action == 0 or action == 1:
        # User inputs
        name = action_name()
        op_manpower = add_manpower('Operational Manpower')
        admin_manpower = add_manpower('Administrative Manpower')
        students = add_manpower('Students')
        st.divider()

        if op_manpower != 0 or admin_manpower != 0 or students != 0:
            new_df, investment = manpower_program([op_manpower, admin_manpower, students],
                                                  action, 'add_action')
            # Calc impact
            budget_imp = total_budget(new_df) - total_budget(st.session_state['df'])
            manpower_imp = total_manpower(new_df) - total_manpower(st.session_state['df'])

            budget_impact(new_df)
            manpower_impact(new_df)
            investments(investment)

            st.divider()

            if st.button('Apply'):

                action_dict = {
                    'action_type': 1,
                    'action': action,
                    'name': name,
                    'op_manpower': op_manpower,
                    'admin_manpower': admin_manpower,
                    'students': students,
                    'budget_impact': budget_imp,
                    'manpower_impact': manpower_imp,
                    'investment': investment
                }
                # Check action has name and not duplicate name
                if check_action_name(action_dict):
                    # Apply action
                    apply_action(action_dict, new_df)

    # Other Programs
    elif action == 2:

        # Make program dataframe in session state
        program_dataframe()
        program_df = st.session_state['program_df']

        name = action_name()
        add_budget_to_program = st.button('Add Budget Row to Program')

        st.divider()

        # Adding row to program and to program_df
        if add_budget_to_program:
            add_budget()

        if len(st.session_state['program_df']) > 0:
            st.subheader('Program', divider=True)
            display_with_delete()


            if st.button('Apply'):

                action_dict = {
                    'action_type': 1,
                    'action': action,
                    'name': name,
                    'takanot': st.session_state['program_df']['Takana'].tolist(),
                    'budget': st.session_state['program_df']['Budget'].tolist(),
                    'budget_impact': st.session_state['program_df']['Budget'].sum(),
                }
                # Check action has name and not duplicate name
                if check_action_name(action_dict):
                    # Making new df with program budgets added to relevant takanot
                    new_df = other_programs(st.session_state['program_df'], 'add_action')
                    # Apply action
                    apply_action(action_dict, new_df)




