import unittest
from unittest.mock import patch

from bill_member import calculate_bill


class TestBillMember(unittest.TestCase):

    @patch('bill_member.get_readings')
    def test_calculate_bill_load_readings(self, mock_get_readings):
        with self.assertRaises(Exception) as context:
            _, _ = calculate_bill('member-123', '2017-08-31')
        assert mock_get_readings.called

    def test_calculate_bill_for_august(self):
        amount, kwh = calculate_bill(
            'member-123',
            '2017-08-31',
            'ALL'
        )
        self.assertEqual(amount, 27.57)
        self.assertEqual(kwh, 167)


if __name__ == '__main__':
    unittest.main()
