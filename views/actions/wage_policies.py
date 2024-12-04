import streamlit as st

from functions.system import initial_check, apply_action
from functions.form_elements import (action_selection, action_name, percent,
                                     budget_impact, manpower_impact, check_action_name)
from functions.budget import (total_budget, total_manpower, wage_increase, minimum_wage_update)


# Check that simulation has been initialized else go back to start page
initial_check()


# Calc new df
def wage_policies_new_df(action, percent, action_status):
    # If general wage increase or automatic wage crawl
    if action == 0 or action == 2:
        # Import relevant function to calc new df
        new_df = wage_increase(st.session_state['df'], percent, action_status)

        return new_df

    # minimum wage update
    elif action == 1:
        # Import relevant function to calc new df
        new_df = minimum_wage_update(st.session_state['df'], percent, action_status)

        return new_df


#################################################
# PAGE
with st.container():
    st.title(':blue[Actions] - Wage Policies')
    st.divider()
    action = action_selection(action_type=2)
    st.divider()
    # If action selected by user
    if action is not None:
        # User inputs
        # Name
        name = action_name()
        # Percent
        percent = percent(action_type=2, action=action)

        # Calc new df
        new_df = wage_policies_new_df(action, percent, 'add_action')
        # Calc impact
        budget_imp = total_budget(new_df) - total_budget(st.session_state['df'])
        manpower_imp = total_manpower(new_df) - total_manpower(st.session_state['df'])

        # Display impact
        budget_impact(new_df)
        manpower_impact(new_df)

        st.divider()

        if st.button('Apply'):

            action_dict = {
                'action_type': 2,
                'action': action,
                'name': name,
                'percent': percent,
                'budget_impact': budget_imp,
                'manpower_impact': manpower_imp
            }
            # Check action has name and not duplicate name
            if check_action_name(action_dict):

                # Apply action
                apply_action(action_dict, new_df)





