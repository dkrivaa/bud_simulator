import streamlit as st

from functions.system import initial_check
from functions.form_elements import budget_model, simulated_budget_summary, action_types


with st.container():
    # Check that simulation has been initialized else go back to start page
    initial_check()

    st.title('Budget Simulator')
    # Display budget model
    budget_model()
    # Display simulated budget summary
    simulated_budget_summary()
    st.divider()
    # Actions
    options = action_types()
    st.subheader(':blue[Add Actions]')
    actions = st.pills(label=':blue[Actions]',
                       label_visibility='hidden',
                       options=options,
                       default=None, )

    # If any action selected
    if actions is not None:
        action = options.index(actions)

        # If quick measures action
        if action == 0:
            st.switch_page('views/actions/quick_measures.py')

        # If programs action
        elif action == 1:
            st.switch_page('views/actions/programs.py')

        # If wage policies action
        elif action == 2:
            st.switch_page('views/actions/wage_policies.py')

    if st.session_state['actions']:
        st.page_link(label=':orange[Actions implemented] - Press here',
                     page='views/actions/summary.py')

    st.divider()

    st.page_link(label='Save / Download Simulation',
                 page='views/save.py')


