import unittest
from datetime import datetime

from accounts import Account
from bill_reading import Reading

"""Unit testing for Account Class"""


class TestAccount(unittest.TestCase):
    READINGS = [{
        "electricity": [
            {
                "cumulative": 18270,
                "readingDate": "2017-06-18T00:00:00.000Z",
                "unit": "kWh"
            },
            {
                "cumulative": 18453,
                "readingDate": "2017-07-31T00:00:00.000Z",
                "unit": "kWh"
            },
            {
                "cumulative": 18620,
                "readingDate": "2017-08-31T00:00:00.000Z",
                "unit": "kWh"
            },
        ],
        "gas": [
            {
                "cumulative": 90,
                "readingDate": "2018-02-19T00:00:00.000Z",
                "unit": "kWh"
            },
            {
                "cumulative": 276,
                "readingDate": "2018-03-14T00:00:00.000Z",
                "unit": "kWh"
            },
            {
                "cumulative": 600,
                "readingDate": "2018-04-29T00:00:00.000Z",
                "unit": "kWh"
            }
        ]

    }]

    def test_init_account_id(self):
        account = Account('account-acc', self.READINGS)
        self.assertEqual(account.account_id, 'account-acc')

    def test_init_billing_readings_len(self):
        account = Account('account-abc', self.READINGS)
        self.assertEqual(len(account.bill_readings['electricity']), 3)
        self.assertEqual(len(account.bill_readings['gas']), 3)

    def test_init_billing_readings_instance(self):
        account = Account('account-abc', self.READINGS)
        self.assertIsInstance(account.bill_readings['electricity'][0], Reading)
        self.assertIsInstance(account.bill_readings['electricity'][1], Reading)
        self.assertIsInstance(account.bill_readings['gas'][0], Reading)
        self.assertIsInstance(account.bill_readings['gas'][1], Reading)

    def test_init_billing_readings_sort(self):
        account = Account('account-abc', self.READINGS)
        self.assertEqual(account.bill_readings['electricity'][1].reading_date, datetime(2017, 7, 31, 0, 0))
        self.assertEqual(account.bill_readings['gas'][2].reading_date, datetime(2018, 4, 29, 0, 0))

    def test_get_month_reading(self):
        account = Account('account-abc', self.READINGS)
        electricity_reading = account.get_month_reading('electricity', datetime(2017, 7, 31, 0, 0))
        gas_reading = account.get_month_reading('gas', datetime(2018, 4, 29, 0, 0))
        self.assertEqual(electricity_reading.reading_date, datetime(2017, 7, 31, 0, 0))
        self.assertEqual(gas_reading.reading_date, datetime(2018, 4, 29, 0, 0))

    def test_calc_monthly_bill_per_type(self):
        account = Account('account-abc', self.READINGS)
        amount, units = account.calc_monthly_bill_per_type('electricity', datetime(2017, 7, 31, 0, 0))
        self.assertEqual(amount, 29.48)
        self.assertEqual(units, 183)

    '''Tested on the scenario of a account having both the gas and electricity but gas billing started on a later 
    date '''
    def test_calculate_monthly_bill(self):
        account = Account('account-abc', self.READINGS)
        amount, units = account.calculate_monthly_bill(datetime(2017, 7, 31, 0, 0))
        self.assertEqual(amount, 29.48)
        self.assertEqual(units, 183)


if __name__ == '__main__':
    unittest.main()
