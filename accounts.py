from calendar import monthrange

from dateutil.relativedelta import relativedelta

from bill_reading import Reading
from tariff import BULB_TARIFF


class Account:
    BILL_TYPES = ('electricity', 'gas')

    def __init__(self, account_id, readings):
        self.account_id = account_id
        self.bill_readings = {}
        for d_reading in readings:
            for billing_type in d_reading:
                if billing_type not in self.BILL_TYPES:
                    raise Exception(f'Incorrect billing energy type -->{billing_type}')
                self.bill_readings[billing_type] = self.gen_readings(d_reading[billing_type])

    def gen_readings(self, bill_reads):
        return sorted([Reading(b_reading) for b_reading in bill_reads], key=lambda i: i.reading_date)

    def get_month_reading(self, bill_type, date_time):
        readings = self.bill_readings[bill_type]
        for reading in readings:
            if reading.reading_date.year == date_time.year and reading.reading_date.month == date_time.month:
                return reading
        return None

    def calc_monthly_bill_per_type(self, billing_type, bill_date):
        try:
            bill_date_read = self.get_month_reading(billing_type, bill_date)
            prev_month_read = self.get_month_reading(billing_type, bill_date - relativedelta(months=1))
            used_units = bill_date_read.cumulative - prev_month_read.cumulative
            num_days_in_month = monthrange(bill_date.year, bill_date.month)[1]
            bill_amount = num_days_in_month * BULB_TARIFF[billing_type]['standing_charge'] + used_units * \
                          BULB_TARIFF[billing_type]['unit_rate']
            return round(bill_amount / 100, 2), used_units
        except:
            return 0, 0

    def calculate_monthly_bill(self, billing_date):
        total_amount = total_units = 0
        for billing_type in self.bill_readings:
            amount, units = self.calc_monthly_bill_per_type(billing_type, billing_date)
            total_amount += amount
            total_units += units
        return total_amount, total_units
