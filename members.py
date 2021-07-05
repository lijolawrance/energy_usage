from accounts import Account


class Member:

    def __init__(self, member_id, readings):
        self.member_id = member_id
        if self.member_id not in readings:
            raise Exception(f'Member ID not available in bill readings {self.member_id}')
        self.accounts = self.gen_accounts_from_bill(readings[self.member_id])

    def gen_accounts_from_bill(self, member_readings):
        d_account = {}
        for account in member_readings:
            account_id = "".join(account.keys())
            d_account[account_id] = Account(account_id, account[account_id])
        return d_account

    '''method to calculate monthly bill for a specific account or for all accounts'''
    def calculate_monthly_bill(self, bill_date, account_id='ALL'):
        total_amount = total_units = 0
        if account_id == 'ALL':
            for account_id in self.accounts:
                amount, units = self.accounts[account_id].calculate_monthly_bill(bill_date)
                total_amount += amount
                total_units += units
            return total_amount, total_units
        else:
            return self.accounts[account_id].calculate_monthly_bill(bill_date)
