import streamlit as st
import pandas as pd
import io
import json

from functions.budget import (total_budget, total_manpower, list_of_takanot,
                              change_quick_measures_action, change_wage_policies_action,
                              change_manpower_programs_action, change_other_programs_action)


def action_types():
    return ['Quick Measures', 'Programs', 'Wage Policies']


def quick_measures_menu():
    return ['Budget cut', 'Manpower cut', 'Price increases']


def programs_menu():
    return ['Establish New Unit', 'Add Manpower to Existing Unit', 'Other Programs']


def wage_policies_menu():
    return ['General Wage Increase', 'Minimum Wage Update', 'Wage Crawling']


def possible_action_keys():
    return ["action_type", "action", "name", "percent", "budget_impact", "manpower_impact",
            "year", "budget_type", "op_manpower", "admin_manpower", "students", "investment",
            "takanot", "budget"]


# Display budget model selected by user
def budget_model():
    year = st.session_state.user_input['year']
    budget_type = st.session_state.user_input['budget_type']
    if year != 20241:
        st.subheader(f'Model: :blue[{year}-{budget_type}]', divider=True)
    else:
        st.subheader(f'Model: :blue[2024-{budget_type}] (Before 7/10/2023)', divider=True)


# Display summary of model budget - total budget and total manpower
def model_budget_summary():
    df_original = st.session_state['df_original']
    st.subheader('Model Summary')
    st.metric(label='Budget - Total',
              value=f'{total_budget(df_original):,.0f}',
              )
    st.metric(label='Manpower - Total',
              value=f'{total_manpower(df_original):,.1f}',
              )


# Display summary of simulation budget - total budget and total manpower
def simulated_budget_summary():
    df = st.session_state['df']
    st.subheader(':orange[Simulated Budget Summary]')
    st.metric(label='Budget - Total',
              value=f'{total_budget(df):,.0f}',
              delta=f'{total_budget(df) - total_budget(st.session_state['df_original']):,.0f}',
              )
    st.metric(label='Manpower - Total',
              value=f'{total_manpower(df):,.1f}',
              delta=f'{total_manpower(df) - total_manpower(st.session_state['df_original']):,.1f}',
              )


# Selection of specific action type action to perform
def action_selection(action_type):
    if action_type == 0:
        options = quick_measures_menu()
    elif action_type == 1:
        options = programs_menu()
    elif action_type == 2:
        options = wage_policies_menu()

    actions = st.pills(label='Select',
                       options=options,
                       default=None)

    if actions is not None:
        return options.index(actions)


# User inputs
# Action name
def action_name():
    return st.text_input(label='Enter Action Name', )


def check_action_name(action_dict):
    # Check if name in action_dict
    if action_dict['name'] is None or action_dict['name'] == '':
        missing_action_name()
        return False
    elif action_dict['name'] in [d.get('name') for d in st.session_state['actions']]:
        duplicate_action_name()
        return False
    return True


@st.dialog('Missing Action Name')
def missing_action_name():
    st.write('Please enter a descriptive action name')

    if st.button('Back'):
        st.rerun()


@st.dialog('Duplicate Action Name')
def duplicate_action_name():
    st.write('Please enter another descriptive action name')

    if st.button('Back'):
        st.rerun()


# percent
def percent(action_type, action):

    # Start value for percent variable
    def start_value(action_type, action):
        label = ''
        value = 0

        # If quick measures
        if action_type == 0:
            # if budget cut
            if action == 0:
                label = 'Percent cut'
                value = 0.5
            # if manpower cut
            elif action == 1:
                label = 'Percent cut'
                value = 1.0
            # if price increase
            elif action == 2:
                label = 'Percent increase'
                value = 2.0

        # Wage policies
        elif action_type == 2:
            # if general wage increase
            if action == 0:
                label = 'Percent increase'
                value = 2.0
            # if minimum wage update
            elif action == 1:
                label = 'Percent increase'
                value = 3.0
            # if wage crawling
            elif action == 2:
                label = 'Percent increase'
                value = 1.5

        return label, value

    # Percent cut
    label, value = start_value(action_type, action)
    percent = st.number_input(label=label,
                              min_value=float(0),
                              step=0.1,
                              value=float(value),
                              format='%0.1f')

    return percent


def add_manpower(manpower_type):
    return st.number_input(label=manpower_type,
                           min_value=float(0),
                           step=1.0,
                           format='%0.1f',
                           key=f'{manpower_type}')


# Display budget impact
def budget_impact(df):
    st.metric(label='Annual Budget Impact',
              value=f"{total_budget(df) - total_budget(st.session_state['df']):,.0f}",
              )


# Display manpower impact
def manpower_impact(df):
    st.metric(label='Manpower impact',
              value=f"{total_manpower(df) - total_manpower(st.session_state['df']):,.0f}",
                  )


# Display Investment
def investments(investment):
    st.metric(label='Investment',
              value=f"{investment:,.0f}",
                  )


def select_takana():
    takanot_list = list_of_takanot(st.session_state['df'])
    return st.selectbox(label='Takana', options=takanot_list)


def program_dataframe():
    columns = ['Takana', 'Budget']

    if 'program_df' not in st.session_state:
        program_df = pd.DataFrame(columns=columns)
        st.session_state['program_df'] = program_df
    else:
        pass


@st.dialog('Add Budget to Program')
def add_budget():
    takana = select_takana()
    budget = st.number_input(label='Budget to add (thousands)',
                             min_value=float(0),
                             step=1000.0,
                             format='%0.1f',)
    if st.button('Add to Program'):
        st.session_state['program_df'].loc[len(st.session_state['program_df'])] = [takana, budget]
        st.rerun()


# Display program df with option to delete row
def display_with_delete():

    def delete_row(index):
        st.session_state['program_df'] = st.session_state['program_df'].drop(index).reset_index(drop=True)

    for idx, row in st.session_state['program_df'].iterrows():
        st.subheader(row['Takana'])
        st.metric(label='Budget',
                  value=f'{row['Budget']:,.0f}')
        # st.write(f'{row['Budget']:,.0f}')
        if st.button(f"Delete", key=f"delete_{idx}"):
            delete_row(idx)
            st.rerun()
    st.divider()
    st.metric(label='Total Budget',
              value=f'{st.session_state['program_df']['Budget'].sum():,.0f}')


# Actions summary
def action_summary(action_type):

    action_list = [d for d in st.session_state['actions'] if d['action_type'] == action_type]
    if len(action_list) == 0:
        st.write('No Actions to Show')
    for d in action_list:
        with st.expander(f'Action - :blue[{d['name']}]'):
            # If quick measures or wage policies
            if action_type == 0 or action_type == 2:
                st.metric(label='Percent',
                          value=f'{d['percent']:,.1f}%')
                st.metric(label='Budget Impact',
                          value=f'{d['budget_impact']:,.0f}')
                st.metric(label='Manpower Impact',
                          value=f'{d['manpower_impact']:,.1f}')
                st.divider()
                # Delete action
                if st.button('Delete', key=f'{d['name']}'):
                    # Update st.session_state['df']
                    # If quick measures
                    if action_type == 0:
                        # Update st.session_state['df']
                        change_quick_measures_action(action_type=action_type,
                                                     action=d['action'],
                                                     percent=d['percent'],
                                                     action_status='cancel_action')
                    elif action_type == 2:
                        # Update st.session_state['df']
                        change_wage_policies_action(action_type=action_type,
                                                    action=d['action'],
                                                    percent=d['percent'],
                                                    action_status='cancel_action')
                    # Delete action from session_state['actions]
                    st.session_state['actions'] = [a for a in st.session_state['actions']
                                                   if a['name'] != d['name']]
                    if len(st.session_state['actions']) > 0:
                        st.rerun()
                    else:
                        st.switch_page('views/simulation.py')
            # If programs
            elif action_type == 1:
                # if Manpower programs
                if d['action'] != 2:
                    st.metric(label='Operational Manpower',
                              value=f'{d['op_manpower']:,.1f}')
                    st.metric(label='Administrative Manpower',
                              value=f'{d['admin_manpower']:,.1f}')
                    st.metric(label='Students',
                              value=f'{d['students']:,.1f}')
                    st.divider()
                    st.metric(label='Annual Budget Impact',
                              value=f'{d['budget_impact']:,.0f}')
                    st.metric(label='Manpower Impact',
                              value=f'{d['manpower_impact']:,.1f}')
                    st.metric(label='Investment',
                              value=f'{d['investment']:,.0f}')
                    st.divider()
                    # Delete action
                    if st.button('Delete', key=f'{d['name']}'):
                        # Update st.session_state['df']
                        change_manpower_programs_action(action_type=action_type,
                                                        action=d['action'],
                                                        op_manpower=d['op_manpower'],
                                                        admin_manpower=d['admin_manpower'],
                                                        students=d['students'],
                                                        action_status='cancel_action')
                        # Delete action from session_state['actions]
                        st.session_state['actions'] = [a for a in st.session_state['actions']
                                                       if a['name'] != d['name']]
                        if len(st.session_state['actions']) > 0:
                            st.rerun()
                        else:
                            st.switch_page('views/simulation.py')

                # Other programs
                elif d['action'] == 2:
                    for i in range(len(d['takanot'])):
                        st.metric(label=d['takanot'][i],
                                  value=f'{d['budget'][i]:,.0f}')
                    st.divider()
                    st.metric(label='Total Budget Impact',
                              value=f'{d['budget_impact']:,.0f}')
                    # Delete action
                    if st.button('Delete', key=f'{d['name']}'):
                        # Update st.session_state['df']
                        change_other_programs_action(action_type=action_type,
                                                     takanot_list=d['takanot'],
                                                     budget_list=d['budget'],
                                                     action_status='cancel_action')
                        # Delete action from session_state['actions]
                        st.session_state['actions'] = [a for a in st.session_state['actions']
                                                       if a['name'] != d['name']]
                        if len(st.session_state['actions']) > 0:
                            st.rerun()
                        else:
                            st.switch_page('views/simulation.py')


def make_excel_budget():
    # Get df ready
    df = st.session_state['df']
    df['קוד תקנה'] = '0' + df['קוד תקנה'].astype(str)
    columns_to_keep = ['קוד תקנה', 'שם תקנה', 'הוצאה נטו', 'שיא כח אדם', 'עבצ', 'כמות']
    df_budget_download = df[columns_to_keep]

    # Convert DataFrame to Excel and return buffer
    buffer = io.BytesIO()
    df_budget_download.to_excel(buffer, index=False, engine='openpyxl')
    buffer.seek(0)

    return buffer


def make_csv_actions():
    action_list = st.session_state['actions']

    # Validate the session state data
    if not isinstance(action_list, list) or not all(isinstance(item, dict) for item in action_list):
        st.error("'actions' must be a list of dictionaries.")
        return None

    # Create DataFrame
    df = pd.DataFrame(action_list)

    # Serialize list columns
    list_columns = ["takanot", "budget"]

    if set(list_columns).issubset(set(df.columns.tolist())):
        for col in list_columns:

            df[col] = df[col].apply(lambda x: json.dumps(x) if isinstance(x, list) else x)

    # Convert to CSV
    return df.to_csv(index=False).encode('utf-8')  # Encode for download



