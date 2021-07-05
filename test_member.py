import unittest
from datetime import datetime

from members import Member

"""Unit testing for Member Class"""


class TestMember(unittest.TestCase):
    READINGS = {
        'member-123': [
            {
                'account-abc': [{
                    "electricity": [
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
                    ]
                }]
            },
            {
                'account-acc': [{
                    "electricity": [
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
                    ]
                }]
            }

        ]
    }

    def test_init_member_id(self):
        member = Member('member-123', self.READINGS)
        self.assertEqual(member.member_id, 'member-123')

    def test_init_id_not_in_readings(self):
        with self.assertRaises(Exception):
            _ = Member('member-123', {})

    def test_init_member_accounts(self):
        member = Member('member-123', {'member-123': [{'account-abc': []}]})
        self.assertIn('account-abc', member.accounts)

    def test_init_accounts(self):
        member = Member('member-123', self.READINGS)
        self.assertIn('account-abc', member.accounts)
        self.assertEqual(len(member.accounts['account-abc'].bill_readings['electricity']), 2)

    def test_calculate_monthly_bill_for_account(self):
        member = Member('member-123', self.READINGS)
        amount, units = member.calculate_monthly_bill(datetime(2017, 8, 31, 0, 0), 'account-abc')
        self.assertEqual(amount, 27.57)
        self.assertEqual(units, 167)

    def test_calculate_monthly_bill(self):
        member = Member('member-123', self.READINGS)
        amount, units = member.calculate_monthly_bill(datetime(2017, 8, 31, 0, 0))
        self.assertEqual(amount, 55.14)
        self.assertEqual(units, 334)


if __name__ == '__main__':
    unittest.main()
