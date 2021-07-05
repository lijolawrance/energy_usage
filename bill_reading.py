from datetime import datetime


class Reading:
    UNIT_TYPE = 'kWh'

    def __init__(self, reading):
        self.reading_date = datetime.strptime(reading['readingDate'][0:10], "%Y-%m-%d")
        self.cumulative = reading['cumulative']
        if reading['unit'] not in self.UNIT_TYPE:
            raise Exception(f"Incorrect unit type {reading['unit']}")
        self.unit = reading['unit']