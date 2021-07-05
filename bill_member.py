from calendar import monthrange
from datetime import datetime

import pandas as pd
from dateutil.relativedelta import relativedelta

from load_readings import get_readings
from members import Member
from tariff import BULB_TARIFF


def calculate_bill(member_id, bill_date, account_id='ALL'):
    billing_date = datetime.strptime(bill_date, "%Y-%m-%d")
    """Partial function implementation using Pandas. Can be used to make the code more simpler"""
    #p_units, p_amount = calc_bill_pandas(
    #    member_id, billing_date, account_id='ALL')
    #print(f'{p_units} and {p_amount}')
    bills = get_readings()
    member = Member(member_id, bills)
    amount, units = member.calculate_monthly_bill(billing_date, account_id)
    return amount, units


def calculate_and_print_bill(member_id, account, bill_date):
    """Calculate the bill and then print it to screen.
    Account is an optional argument - I could bill for one account or many.
    There's no need to refactor this function."""
    member_id = member_id or 'member-123'
    bill_date = bill_date or '2017-08-31'
    account = account or 'ALL'
    amount, kwh = calculate_bill(member_id, bill_date, account)
    print('Hello {member}!'.format(member=member_id))
    print('Your bill for {account} on {date} is £{amount}'.format(
        account=account,
        date=bill_date,
        amount=amount))
    print('based on {kwh}kWh of usage in the last month'.format(kwh=kwh))


'''''''''''''''''''''''''''''''''Pandas based solution '''''''''''''''''''''''''''''''''


def load_dataframe(member_id, account_id='ALL'):
    final_flattened_df = pd.DataFrame()
    read = get_readings()
    if account_id == 'ALL':
        df_member = pd.json_normalize(read['member-123'])
    else:
        df_member = pd.json_normalize(
            read['member-123'], account_id, errors='ignore')
    final_df = pd.DataFrame()
    for i in df_member:
        df_account = pd.json_normalize(
            read[member_id], [df_member[i].name], errors='ignore')
        for j in df_account:
            # print(df_account[j].name)
            df_bill_type = pd.json_normalize(
                read[member_id], [df_member[i].name, df_account[j].name], errors='ignore')
            df_bill_type['member'] = member_id
            df_bill_type['account'] = df_member[i].name
            df_bill_type['type'] = df_account[j].name
            df_bill_type['formatted_date'] = pd.to_datetime(
                df_bill_type['readingDate']).dt.date
            df_bill_type['formatted_month'] = pd.to_datetime(
                df_bill_type['readingDate']).dt.month
            df_bill_type['formatted_year'] = pd.to_datetime(
                df_bill_type['readingDate']).dt.year
            final_flattened_df = final_df.append(
                df_bill_type, ignore_index=True)
    del df_member, df_account, df_bill_type
    return final_flattened_df


def calc_bill_pandas(member_id, bill_date, account_id='ALL'):
    used_units = bill_amount = 0
    prev_month = bill_date - relativedelta(months=1)
    # print(prev_month.year)
    df_readings = load_dataframe(member_id, account_id)
    if account_id == 'ALL':
        accounts = df_readings['account'].unique()
    else:
        accounts = df_readings.loc[df_readings['account'] == account_id]
    for account in accounts:
        types = df_readings['type'].unique()
        for bill_type in types:
            df_reading_t = df_readings.where(
                (df_readings['account'] == account) & (df_readings['type'] == bill_type)).dropna()
            current_reading = df_reading_t[(df_reading_t['formatted_month'] == bill_date.month)
                                           & (df_reading_t['formatted_year'] == bill_date.year)]
            previous_reading = df_reading_t[(df_reading_t['formatted_month'] == prev_month.month)
                                            & (df_reading_t['formatted_year'] == prev_month.year)]
            used_units = int(
                current_reading['cumulative']) - int(previous_reading['cumulative'])
            num_days_in_month = monthrange(bill_date.year, bill_date.month)[1]
            bill_amount = num_days_in_month * BULB_TARIFF[bill_type]['standing_charge'] + used_units * \
                BULB_TARIFF[bill_type]['unit_rate']
    return used_units, round(bill_amount / 100, 2)
