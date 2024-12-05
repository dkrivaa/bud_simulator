import streamlit as st

from functions.system import initial_check, check_actions


# Check that simulation has been initialized else go back to start page
initial_check()
# # Check that there are actions
check_actions()

