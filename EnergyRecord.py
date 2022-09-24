import datetime
from decimal import *
from bson.decimal128 import Decimal128

class EnergyRecord:
    import datetime
    def __init__(self, record=None, data_line=None, source_type=None):
        if data_line:
            self.id = id
            self.source_type = source_type
            self.date = None
            self.time = None
            self.duration = None
            self.reading = 0.0
            self.process_line(data_line)
        elif record:
            self.id = record['_id']
            self.source_type = record['source_type']
            self.date = record['date']
            self.duration = record['duration']
            self.reading = record['reading']

    def process_line(self, line):
        delimit = line.split(',')
        delimit = [element.replace("+01:00", "").replace("+00:00","") for element in delimit]
        time_field = delimit[1].replace('T',' ').strip()
        self.date = datetime.datetime.strptime(time_field, '%Y-%m-%d %H:%M:%S')
        self.duration = 30
        self.reading = str(delimit[0])

    def record_as_dict(self):
        return {'source_type' : self.source_type, 'date' : self.date, 'duration' : self.duration, 'reading' : self.reading}

    def __str__(self):
        return(f"'source_type' : '{self.source_type}', 'date' : {self.date}, 'duration' : {self.duration}, 'reading' : {self.reading}")
