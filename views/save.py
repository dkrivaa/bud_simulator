import streamlit as st

from functions.system import initial_check, check_actions
from functions.form_elements import make_excel_budget, make_csv_actions


# Check that simulation has been initialized else go back to start page
initial_check()
# Check that there are actions
check_actions()


st.title('Save & Download Simulation')
st.divider()

# Get Excel buffer
buffer = make_excel_budget()

st.write('Download Simulator Budget as Excel')
st.download_button(
    label='Download Budget (Excel)',
    data=buffer,
    file_name='Budget.xlsx',
    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    key='Excel'
    )

st.divider()

# Get CSV action data
csv_data = make_csv_actions()
st.write('Download Simulator for Future Upload (csv)')
if csv_data:
    st.download_button(
                label="Download Simulation (CSV)",
                data=csv_data,
                file_name="Simulation.csv",
                mime="text/csv",
                key='csv'
            )
