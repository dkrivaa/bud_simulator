import streamlit as st


# Initializing basic session state for simulation
def startup():
    # Clear session_state
    st.session_state.clear()
    # Define dict to hold user inputs
    st.session_state.user_input = {}
    # Define list to hold actions
    st.session_state['actions'] = []


# Define budget model - year and budget type
def budget_model(year, budget_type):
    if 'user_input' in st.session_state:
        # Save year and budget type selected by user
        st.session_state.user_input['year'] = year
        st.session_state.user_input['budget_type'] = budget_type
    else:
        error_start_simulation()


@st.dialog('No Active Simulation')
def error_start_simulation():
    st.write('Please start new simulation or upload saved simulation')
    if st.button('Back', key='error_start_simulation'):
        st.switch_page('views/start.py')


# Check that simulation has been initialized
def initial_check():
    if 'user_input' not in st.session_state:
        # Create a placeholder for the "modal"
        placeholder = st.empty()

        with placeholder.container():
            st.warning("Please Start New / Upload Simulation")
            if st.button("Continue"):
                placeholder.empty()  # Close the "modal"
                st.switch_page("views/start.py")

        # Prevent other UI interactions by not rendering additional elements
        st.stop()


# Redirect if no actions
def check_actions():

    if len(st.session_state['actions']) == 0:
        # Create a placeholder for the "modal"
        placeholder = st.empty()

        with placeholder.container():
            st.warning("Nothing to Save / Download (No actions made)")
            if st.button("Continue"):
                placeholder.empty()  # Close the "modal"
                st.switch_page("views/simulation.py")

        # Prevent other UI interactions by not rendering additional elements
        st.stop()


# Apply action
def apply_action(action_dict, new_df):
    # Add year and budget type to action dict
    action_dict['year'] = st.session_state.user_input['year']
    action_dict['budget_type'] = st.session_state.user_input['budget_type']
    # Add action to session_state list of actions
    st.session_state['actions'].append(action_dict)
    # Update budget df in session_state['df']
    st.session_state['df'] = new_df

    if 'program_df' in st.session_state:
        del st.session_state['program_df']

    st.switch_page('views/simulation.py')
