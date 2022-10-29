import pandas
import datetime
from dateutil import parser

def aggregate_data(data, aggregation):
    end_record_date = data[0].date
    start_record_date = data[-1].date
    aggregate_response = []
    time_range = pandas.date_range(start_record_date, end_record_date, freq=aggregation.upper())
    time_stamps = [parser.parse(str(x)) for x in time_range]
    if aggregation=='h':
        for time_stamp in time_stamps:
            active_record = aggregate_records_by_hour(data, time_stamp)
            aggregate_response.append(active_record)

    elif aggregation=='d':
        for time_stamp in time_stamps:
            active_record= aggregate_records_by_day(data, time_stamp)
            aggregate_response.append(active_record)
    return aggregate_response


def aggregate_records_by_hour(data, time_stamp):
    range_values = [time_stamp.year, time_stamp.month, time_stamp.day, time_stamp.hour]
    group = [agg for agg in data if [agg.date.year, agg.date.month, agg.date.day, agg.date.hour] == range_values]
    group.sort(key=lambda a: a.date)
    active_record = group[0]
    active_record.reading = sum(rec.reading for rec in group)
    active_record.duration = 60
    return active_record

def aggregate_records_by_day(data, time_stamp):
    range_values = [time_stamp.year, time_stamp.month, time_stamp.day]
    group = [agg for agg in data if [agg.date.year, agg.date.month, agg.date.day] == range_values]
    group.sort(key=lambda a: a.date)
    active_record = group[0]
    active_record.reading = sum(rec.reading for rec in group)
    active_record.duration = 1440
    return active_record


def aggregate_by_day(data):
    start_date = data[0].date
    end_date = data[-1].date
    delta = end_date - start_date

    aggregation = {}

    for iterator in range(0, delta.days):
        current_date = start_date + datetime.timedelta(days = iterator)
        sub_set = [element for element in data if (element.date.year == current_date.year and element.date.month == current_date.month and element.date.day == current_date.day)]
        summed = sum(float(readings.reading) for readings in sub_set )
        date_value = f"{current_date.year}-{current_date.month}-{current_date.day}"
        aggregation[date_value] = summed

    return aggregation