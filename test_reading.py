import unittest
from datetime import datetime

from bill_reading import Reading


class TestReading(unittest.TestCase):
    CORRECT = {
        "cumulative": 18270,
        "readingDate": "2017-06-18T00:00:00.000Z",
        "unit": "kWh"
    }

    INVALID = {
        "cumulative": 18270,
        "readingDate": "2017-06-18T00:00:00.000Z",
        "unit": "Energy"
    }

    def test_init_read_date(self):
        reading = Reading(self.CORRECT)
        assert reading.reading_date == datetime(2017, 6, 18, 0, 0)

    def test_init_cumulative(self):
        reading = Reading(self.CORRECT)
        assert reading.cumulative == 18270

    def test_init_unit(self):
        reading = Reading(self.CORRECT)
        assert reading.unit == 'kWh'

    '''def test_init_invalid_unit(self):
        with self.assertRaises(Exception) as context:
            reading = Reading(self.INVALID)'''


if __name__ == '__main__':
    unittest.main()
