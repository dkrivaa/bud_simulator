import streamlit as st
import pandas as pd


def assumptions():
    return {
        'operational_standby': 5.5 * 12,  # Number of standby hours for single operational manpower
        'admin_standby': 5.5,  # Number of standby hours for single admin manpower
        'student_hours': 96,  # Monthly work hours for single student
        'new_unit_operational_investment': 750,  # Investment needed per operational manpower in new unit
        'new_unit_admin_investment': 300,  # Investment needed per admin manpower in new unit
        'existing_unit_operational_investment': 250,  # Investment needed per operational manpower in existing unit
        'existing_unit_admin_investment': 50,  # Investment needed per admin manpower in existing unit
        'fixed_operation': 20,
        'op_ex': 0.1  # Operating cost as % of investment
    }


# General budget
# Total Budget
def total_budget(df):
    return df['הוצאה נטו'].sum()


# Total Wage Budget
def total_wage_budget(df):
    return df.loc[(df['קוד מיון רמה 1'] == 1) | ((df['קוד מיון רמה 1'] == 19) &
                                                 (df['שם תכנית'] == 'שכר')), 'הוצאה נטו'].sum()


# Total Operation Budget
def total_operational_budget(df):
    return total_budget(df) - total_wage_budget(df)


# Manpower + manpower budgets
def total_sie_manpower_amount(df):
    return df.loc[df['שיא כח אדם'] > 0, 'שיא כח אדם'].sum()


def total_sie_manpower_budget(df):
    return df.loc[df['שיא כח אדם'] > 0, 'הוצאה נטו'].sum()


def temp_manpower_amount(df):
    return df.loc[df['עבצ'] > 0, 'עבצ'].sum() / 12


def temp_manpower_budget(df):
    return df.loc[df['עבצ'] > 0, 'הוצאה נטו'].sum()


def total_manpower(df):
    return total_sie_manpower_amount(df) + df.loc[df['עבצ'] > 0, 'עבצ'].sum() / 12


def admin_manpower_amount(df):
    return df.loc[df['קוד תקנה'] == 7600114, 'שיא כח אדם'].sum()


def admin_manpower_budget(df):
    return df.loc[df['קוד תקנה'] == 7600114, 'הוצאה נטו'].sum()


def new_op_manpower_amount(df):
    return df.loc[df['קוד תקנה'] == 7600112, 'שיא כח אדם'].sum()


def new_op_manpower_budget(df):
    return df.loc[df['קוד תקנה'] == 7600112, 'הוצאה נטו'].sum()


def old_op_manpower_amount(df):
    return df.loc[df['קוד תקנה'] == 7600113, 'שיא כח אדם'].sum()


def old_op_manpower_budget(df):
    return df.loc[df['קוד תקנה'] == 7600113, 'הוצאה נטו'].sum()


# Overtime
def admin_overtime_amount(df):
    return df.loc[df['קוד תקנה'] == 7600105, 'כמות'].sum()


def admin_overtime_budget(df):
    return df.loc[df['קוד תקנה'] == 7600105, 'הוצאה נטו'].sum()


def new_op_overtime_amount(df):
    return df.loc[df['קוד תקנה'] == 7600118, 'כמות'].sum()


def new_op_overtime_budget(df):
    return df.loc[df['קוד תקנה'] == 7600118, 'הוצאה נטו'].sum()


def old_op_overtime_amount(df):
    return df.loc[df['קוד תקנה'] == 7600119, 'כמות'].sum()


def old_op_overtime_budget(df):
    return df.loc[df['קוד תקנה'] == 7600119, 'הוצאה נטו'].sum()


def total_overtime_amount(df):
    return (admin_overtime_amount(df) +
            new_op_overtime_amount(df) +
            old_op_overtime_amount(df))


def total_overtime_budget(df):
    return (admin_overtime_budget(df) +
            new_op_overtime_budget(df) +
            old_op_overtime_budget(df))


# Standby
def standby_amount(df):
    return df.loc[df['קוד תקנה'] == 7600107, 'כמות'].sum()


def standby_budget(df):
    return df.loc[df['קוד תקנה'] == 7600107, 'הוצאה נטו'].sum()


# Car reimbursement
def car_reimbursement_amount(df):
    return df.loc[df['קוד תקנה'] == 7600104, 'כמות'].sum()


def car_reimbursement_budget(df):
    return df.loc[df['קוד תקנה'] == 7600104, 'הוצאה נטו'].sum()


# Students
def students_amount(df):
    student_hours = assumptions()['student_hours']
    return df.loc[df['קוד תקנה'] == 7600103, 'כמות'].sum() / student_hours / 12


def students_budget(df):
    return df.loc[df['קוד תקנה'] == 7600103, 'הוצאה נטו'].sum()


def national_service_budget(df):
    return df.loc[df['קוד תקנה'] == 7600108, 'הוצאה נטו'].sum()


def national_service_amount(df):
    national_service_cost = 50
    return national_service_budget(df) / national_service_cost


# QUICK MEASURES
# Flat operational budget cut
def operational_budget_cut(df, percent, action_status):
    percent = percent / 100
    df_temp = df.copy()
    df_original = st.session_state['df_original'].copy()

    def condition(df_condition):
        return (df_condition['קוד מיון רמה 1'] != 1) | ((df_condition['קוד מיון רמה 1'] == 19) &
                                                        (df_condition['שם תכנית'] != 'שכר')), 'הוצאה נטו'

    df_original.loc[condition(df_original)] *= percent

    if action_status == 'add_action':
        df_temp.loc[condition(df_temp)] -= df_original.loc[condition(df_original)]
    elif action_status == 'cancel_action':
        df_temp.loc[condition(df_temp)] += df_original.loc[condition(df_original)]

    return df_temp


# Flat manpower cut incl. overtime, standby and car reimbursement
def manpower_cut(df, percent, action_status):
    percent = percent / 100
    df_temp = df.copy()
    df_original = st.session_state['df_original'].copy()

    # Manpower amount - sie
    def condition1(df_condition):
        return df_condition['שיא כח אדם'] > 0, 'שיא כח אדם'

    df_original.loc[condition1(df_original)] *= percent
    if action_status == 'add_action':
        df_temp.loc[condition1(df_temp)] -= df_original.loc[condition1(df_original)]
    elif action_status == 'cancel_action':
        df_temp.loc[condition1(df_temp)] += df_original.loc[condition1(df_original)]

    # Manpower budget - sie
    def condition2(df_condition):
        return df_condition['שיא כח אדם'] > 0, 'הוצאה נטו'

    df_original.loc[condition2(df_original)] *= percent
    if action_status == 'add_action':
        df_temp.loc[condition2(df_temp)] -= df_original.loc[condition2(df_original)]
    elif action_status == 'cancel_action':
        df_temp.loc[condition2(df_temp)] += df_original.loc[condition2(df_original)]

    # Manpower amount - abatz
    def condition3(df_condition):
        return df_condition['עבצ'] > 0, 'עבצ'

    df_original.loc[condition3(df_original)] *= percent
    if action_status == 'add_action':
        df_temp.loc[condition3(df_temp)] -= df_original.loc[condition3(df_original)]
    elif action_status == 'cancel_action':
        df_temp.loc[condition3(df_temp)] += df_original.loc[condition3(df_original)]

    # Manpower budget - abatz
    def condition4(df_condition):
        return df_condition['עבצ'] > 0, 'הוצאה נטו'

    df_original.loc[condition4(df_original)] *= percent
    if action_status == 'add_action':
        df_temp.loc[condition4(df_temp)] -= df_original.loc[condition4(df_original)]
    elif action_status == 'cancel_action':
        df_temp.loc[condition4(df_temp)] += df_original.loc[condition4(df_original)]

    # Overtime (X3), standby and car reimbursement - amount and budget
    for takana in [7600105, 7600118, 7600119, 7600107, 7600104]:

        def condition5(df_condition):
            return df_condition['קוד תקנה'] == takana, 'כמות'

        df_original.loc[condition5(df_original)] *= percent
        if action_status == 'add_action':
            df_temp.loc[condition5(df_temp)] -= df_original.loc[condition5(df_original)]
        elif action_status == 'cancel_action':
            df_temp.loc[condition5(df_temp)] += df_original.loc[condition5(df_original)]

        def condition6(df_condition):
            return df_condition['קוד תקנה'] == takana, 'הוצאה נטו'

        df_original.loc[condition6(df_original)] *= percent
        if action_status == 'add_action':
            df_temp.loc[condition6(df_temp)] -= df_original.loc[condition6(df_original)]
        elif action_status == 'cancel_action':
            df_temp.loc[condition6(df_temp)] += df_original.loc[condition6(df_original)]

    return df_temp


# Price increases
def price_increase(df, percent, action_status):
    percent = percent / 100
    df_temp = df.copy()
    df_original = st.session_state['df_original'].copy()

    def condition(df_condition):
        return ((df_condition['קוד מיון רמה 1'] != 1) |
                ((df_condition['קוד מיון רמה 1'] == 19) & (df_condition['שם תכנית'] != 'שכר')) |
                (df_condition['קוד תקנה'] == 7600104), 'הוצאה נטו')

    df_original.loc[condition(df_original)] *= percent

    if action_status == 'add_action':
        df_temp.loc[condition(df_temp)] += df_original.loc[condition(df_original)]
    elif action_status == 'cancel_action':
        df_temp.loc[condition(df_temp)] -= df_original.loc[condition(df_original)]

    return df_temp


# WAGE POLICIES
# Wage increase
def wage_increase(df, percent, action_status):
    percent = percent / 100
    df_temp = df.copy()
    df_original = st.session_state['df_original'].copy()

    # Manpower budget
    def condition1(df_condition):
        return df_condition['שיא כח אדם'] > 0, 'הוצאה נטו'

    df_original.loc[condition1(df_original)] *= percent
    if action_status == 'add_action':
        df_temp.loc[condition1(df_temp)] += df_original.loc[condition1(df_original)]
    elif action_status == 'cancel_action':
        df_temp.loc[condition1(df_temp)] -= df_original.loc[condition1(df_original)]

    def condition2(df_condition):
        return df_condition['עבצ'] > 0, 'הוצאה נטו'

    df_original.loc[condition2(df_original)] *= percent
    if action_status == 'add_action':
        df_temp.loc[condition2(df_temp)] += df_original.loc[condition2(df_original)]
    elif action_status == 'cancel_action':
        df_temp.loc[condition2(df_temp)] -= df_original.loc[condition2(df_original)]

    # Overtime (X3), standby - amount and budget
    for takana in [7600105, 7600118, 7600119, 7600107]:

        def condition3(df_condition):
            return df_original['קוד תקנה'] == takana, 'כמות'

        df_original.loc[condition3(df_original)] *= percent
        if action_status == 'add_action':
            df_temp.loc[condition3(df_temp)] += df_original.loc[condition3(df_original)]
        elif action_status == 'cancel_action':
            df_temp.loc[condition3(df_temp)] -= df_original.loc[condition3(df_original)]

        def condition4(df_condition):
            return df_condition['קוד תקנה'] == takana, 'הוצאה נטו'

        df_original.loc[condition4(df_original)] *= percent
        if action_status == 'add_action':
            df_temp.loc[condition4(df_temp)] += df_original.loc[condition4(df_original)]
        elif action_status == 'cancel_action':
            df_temp.loc[condition4(df_temp)] -= df_original.loc[condition4(df_original)]

    return df_temp


# Minimum wage increase
def minimum_wage_update(df, percent, action_status):
    percent = percent / 100
    df_temp = df.copy()
    df_original = st.session_state['df_original'].copy()

    # Students
    def condition(df_condition):
        return df_condition['קוד תקנה'] == 7600103, 'הוצאה נטו'

    df_original.loc[condition(df_original)] *= percent
    if action_status == 'add_action':
        df_temp.loc[condition(df_temp)] -= df_original.loc[condition(df_original)]
    elif action_status == 'cancel_action':
        df_temp.loc[condition(df_temp)] += df_original.loc[condition(df_original)]

    # General manpower
    df_update = wage_increase(df_temp, percent * 100 / 3, action_status)

    # Not saving df_temp - it is being saved by wage_increase function (df_update)
    return df_update


# Manpower programs
# Cost of adding manpower
def manpower_program(manpower_list, unit_status, action_status):
    df = st.session_state['df']
    df_temp = df.copy()
    df_original = st.session_state['df_original'].copy()

    def manpower_types(manpower_type):
        types = {
            'operational': 1,
            'admin': 2,
            'students': 3
        }
        return types[manpower_type]

    def add_to_df_wage(dict, man_type, cost, manpower_amount, action_status):
        if action_status == 'add_action':
            df_temp.loc[df_temp['קוד תקנה'] == dict[man_type], 'הוצאה נטו'] += cost
            if dict[man_type] == 7600112 or dict[man_type] == 7600114:
                df_temp.loc[df_temp['קוד תקנה'] == dict[man_type], 'שיא כח אדם'] += manpower_amount
            else:
                df_temp.loc[df_temp['קוד תקנה'] == dict[man_type], 'כמות'] += manpower_amount
        elif action_status == 'cancel_action':
            df_temp.loc[df_temp['קוד תקנה'] == dict[man_type], 'הוצאה נטו'] -= cost
            if dict[man_type] == 7600112 or dict[man_type] == 7600114:
                df_temp.loc[df_temp['קוד תקנה'] == dict[man_type], 'שיא כח אדם'] -= manpower_amount
            else:
                df_temp.loc[df_temp['קוד תקנה'] == dict[man_type], 'כמות'] -= manpower_amount

    def add_to_df_costs(takana, cost, action_status):
        if action_status == 'add_action':
            df_temp.loc[df_temp['קוד תקנה'] == takana, 'הוצאה נטו'] += cost
        elif action_status == 'cancel_action':
            df_temp.loc[df_temp['קוד תקנה'] == takana, 'הוצאה נטו'] -= cost

    def basic_wage(manpower_type, manpower_amount):
        man_type = manpower_types(manpower_type)

        basic_wage_takanot = {
            1: 7600112,
            2: 7600114,
            3: 7600103
        }

        if man_type == 1:
            cost = (new_op_manpower_budget(df_original) / new_op_manpower_amount(df_original)) * manpower_amount
            # st.write('basic wage', cost)
            add_to_df_wage(basic_wage_takanot, man_type, cost, manpower_amount, action_status)
        elif man_type == 2:
            cost = (admin_manpower_budget(df_original) / admin_manpower_amount(df_original)) * manpower_amount
            # st.write('basic wage', cost)
            add_to_df_wage(basic_wage_takanot, man_type, cost, manpower_amount, action_status)
        elif man_type == 3:
            cost = (students_budget(df_original) / students_amount(df_original)) * manpower_amount
            # st.write('basic wage', cost)
            add_to_df_wage(basic_wage_takanot, man_type, cost, manpower_amount * 12 * assumptions()['student_hours'], action_status)

    def overtime_cost(manpower_type, manpower_amount):
        man_type = manpower_types(manpower_type)

        overtime_takanot = {
            1: 7600118,
            2: 7600105
        }

        if man_type == 1:
            average_hours = new_op_overtime_amount(df_original) / new_op_manpower_amount(df_original)
            average_cost = new_op_overtime_budget(df_original) / new_op_overtime_amount(df_original)
            cost = average_hours * average_cost * manpower_amount
            amount = average_hours * manpower_amount
            add_to_df_wage(overtime_takanot, man_type, cost, amount, action_status)
        elif man_type == 2:
            average_hours = admin_overtime_amount(df_original) / admin_manpower_amount(df_original)
            average_cost = admin_overtime_budget(df_original) / admin_overtime_amount(df_original)
            cost = average_hours * average_cost * manpower_amount
            amount = average_hours * manpower_amount
            add_to_df_wage(overtime_takanot, man_type, cost, amount, action_status)

    def standby_cost(manpower_type, manpower_amount):
        man_type = manpower_types(manpower_type)

        standby_takana = {
            1: 7600107,
            2: 7600107
        }

        if man_type == 1:
            cost = ((standby_budget(df_original) / standby_amount(df_original)) * manpower_amount *
                    assumptions()['operational_standby'])
            amount = manpower_amount * assumptions()['operational_standby']
            add_to_df_wage(standby_takana, man_type, cost, amount, action_status)
        elif man_type == 2:
            cost = ((standby_budget(df_original) / standby_amount(df_original)) * manpower_amount *
                    assumptions()['admin_standby'])
            amount = manpower_amount * assumptions()['admin_standby']
            add_to_df_wage(standby_takana, man_type, cost, amount, action_status)

    def car_reimbursement(manpower_type, manpower_amount):
        man_type = manpower_types(manpower_type)

        car_reimbursement_takana = {
            1: 7600104,
            2: 7600104
        }

        if man_type == 1 or man_type == 2:
            average_cost = car_reimbursement_budget(df_original) / car_reimbursement_amount(df_original)
            average_amount = car_reimbursement_amount(df_original) / total_manpower(df_original)
            cost = average_cost * average_amount * manpower_amount
            amount = average_amount * manpower_amount
            add_to_df_wage(car_reimbursement_takana, man_type, cost, amount, action_status)

    def cap_ex(manpower_type, manpower_amount, unit_status):
        man_type = manpower_types(manpower_type)

        if unit_status == 0:
            if man_type == 1:
                cost = assumptions()['new_unit_operational_investment'] * manpower_amount
                op_ex = cost * assumptions()['op_ex'] + assumptions()['fixed_operation'] * manpower_amount
                return cost, op_ex
            elif man_type == 2 or man_type == 3:
                cost = assumptions()['new_unit_admin_investment'] * manpower_amount
                op_ex = cost * assumptions()['op_ex'] + assumptions()['fixed_operation'] * manpower_amount
                return cost, op_ex

        elif unit_status == 1:
            if man_type == 1:
                cost = assumptions()['existing_unit_operational_investment'] * manpower_amount
                op_ex = cost * assumptions()['op_ex'] + assumptions()['fixed_operation'] * manpower_amount
                return cost, op_ex
            elif man_type == 2 or man_type == 3:
                cost = assumptions()['existing_unit_admin_investment'] * manpower_amount
                op_ex = cost * assumptions()['op_ex'] + assumptions()['fixed_operation'] * manpower_amount
                return cost, op_ex

    # Running the functions
    investment = 0
    operation = 0
    for i in range(len(manpower_list)):
        manpower_types_list = ['operational', 'admin', 'students']
        manpower = manpower_list[i]
        manpower_type = manpower_types_list[i]

        # Making the calcs and adding to st.session_state['df_temp']
        basic_wage(manpower_type, manpower)  # Basic wage
        overtime_cost(manpower_type, manpower)  # overtime cost & overtime amount
        standby_cost(manpower_type, manpower)  # standby cost & standby amount
        car_reimbursement(manpower_type, manpower)  # car reimbursement cost & car reimbursement amount
        invest, op_ex = cap_ex(manpower_type, manpower, unit_status)
        investment += invest
        operation += op_ex

    add_to_df_costs(7600221, operation, action_status)

    return df_temp, investment


# Other programs
def other_programs(df_temp, action_status):
    # df_temp is a df from takanot list and budget list in program
    df_temp = split_takana(df_temp)
    df_temp = add_amounts(df_temp)

    df_new = st.session_state['df'].copy()

    # list of takanot in program
    program_takanot_list = df_temp['takana_num'].unique().tolist()

    for takana in program_takanot_list:

        # Add program budgets to df_new
        if action_status == 'add_action':
            df_new.loc[df_new['קוד תקנה'] == takana, 'הוצאה נטו'] += df_temp.loc[
                df_temp['takana_num'] == takana, 'Budget'].sum()
            # Add program amounts to df_new
            df_new.loc[df_new['קוד תקנה'] == takana, 'כמות'] += df_temp.loc[
                df_temp['takana_num'] == takana, 'amount'].sum()
        elif action_status == 'cancel_action':
            # detract program budgets from df_new
            df_new.loc[df_new['קוד תקנה'] == takana, 'הוצאה נטו'] -= df_temp.loc[
                df_temp['takana_num'] == takana, 'Budget'].sum()
            # detract program amounts from df_new
            df_new.loc[df_new['קוד תקנה'] == takana, 'כמות'] -= df_temp.loc[
                df_temp['takana_num'] == takana, 'amount'].sum()

    return df_new


# Help function for 'other_programs' function
def split_takana(df):
    # Splitting the takana number - takana name into two columns
    df[['takana_num', 'name']] = df['Takana'].str.split(pat='-', n=1, expand=True)
    # Turning 'takana_num' into number
    df['takana_num'] = df['takana_num'].astype(int)
    return df


# Help function for 'other_programs' function
# If takana with added budget is a takana with amounts, the corresponding amount is added to amount column
def add_amounts(df):
    df_original = st.session_state['df_original'].copy()
    amount_takanot_list = [7600103, 7600104, 7600105, 7600107, 7600118, 7600119]

    average_dict = {}
    # Ensure no division by zero or missing values in the calculation
    for tak in amount_takanot_list:
        # Filter rows where 'קוד תקנה' matches 'tak'
        net_expense = df_original.loc[df_original['קוד תקנה'] == tak, 'הוצאה נטו']
        quantity = df_original.loc[df_original['קוד תקנה'] == tak, 'כמות']

        # Avoid division by zero
        if not quantity.empty and quantity.sum() != 0:
            average_dict[tak] = (quantity.sum() / net_expense.sum())
        else:
            average_dict[tak] = 0  # Assign 0 if the calculation isn't possible

        # Update the 'amount' column in df_temp for matching rows
        df.loc[df['takana_num'] == tak, 'amount'] = (
            df.loc[df['takana_num'] == tak, 'Budget'] * average_dict[tak] * 1000
            if average_dict[tak] != 0 else 0
        )

        # Fill all missing values with 0
        df.fillna(0, inplace=True)

    return df


# List of takanot
def list_of_takanot(df):
    return df['קוד ושם תקנה'].unique().tolist()


# Delete quick measures action from simulated budget
def change_quick_measures_action(action_type, action, percent, action_status):
    df = st.session_state['df'].copy()
    # If budget cut
    if action == 0:
        new_df = operational_budget_cut(df, percent, action_status)
    # If manpower cut
    elif action == 1:
        new_df = manpower_cut(df, percent, action_status)
    # If price increase
    elif action == 2:
        new_df = price_increase(df, percent, action_status)

    st.session_state['df'] = new_df


# Delete wage policies action from simulated budget
def change_wage_policies_action(action_type, action, percent, action_status):
    df = st.session_state['df'].copy()
    # If general wage increase or wage crawling
    if action == 0 or action == 2:
        new_df = wage_increase(df, percent, action_status)
    # If minimum wage update
    elif action == 1:
        new_df = minimum_wage_update(df, percent, action_status)

    st.session_state['df'] = new_df


# Delete manpower programs
def change_manpower_programs_action(action_type, action, op_manpower, admin_manpower, students, action_status):
    new_df, investment = manpower_program([op_manpower, admin_manpower, students],
                              action, action_status)
    st.session_state['df'] = new_df


# Delete other programs
def change_other_programs_action(action_type, takanot_list, budget_list, action_status):
    df_temp = pd.DataFrame({'Takana': takanot_list, 'Budget': budget_list})
    new_df = other_programs(df_temp, action_status)
    st.session_state['df'] = new_df






