import datetime

import bson

from Mongo import *
from data import *
from EnergyRecord import EnergyRecord



def parse_file(file_name):
    with open(file_name, "r") as file:
        file_content = file.readlines()
    if 'kWh' in file_content[0]:
        collection_name = 'electricity'
    else:
        collection_name = "gas"

    parsed_data =[]

    for iterate_count in range (1,len(file_content)):
        print(iterate_count)
        record = EnergyRecord(data_line=file_content[iterate_count],   source_type=collection_name)
        parsed_data.append(record.record_as_dict())
    print(parsed_data)
    return parsed_data


def write_to_mongo(db, content, collection):
    db.initialise_db(collection)
    db.insert_data(collection, content)

def read_from_mongo(db, collection, query):
    db.initialise_db(collection)
    return db.get_data(collection, query)

def connect():
    return mongo_db(connection_string, password)

def load_from_file(databse, collection, file_name):
    data_to_load = parse_file(file_name)
    write_to_mongo(databse, data_to_load, collection)

def send_data_to_graph(data):
    contents = None
    with open("data_graph.html", "r") as in_file, open("data_graph_populated.html", "w") as out_file:
        contents = in_file.read()
        contents = contents.replace("xxnumberpointsxx", f"{len(data)}")
        contents = contents.replace("xxdataxx",str(data))

        out_file.write(contents)


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


def main():
    db = connect()
    collection_name = "energy"

    #load_from_file(db,"energy", "../electricity.csv")
    #load_from_file(db,"energy","../gas.csv")



    data = read_from_mongo(db, collection_name,  {'source_type': 'electricity'})
    record_collection = []
    for rec in data:
        record_collection.append(EnergyRecord(rec))
    aggregated_data = aggregate_by_day(record_collection)
    list_aggregation = list(aggregated_data.values())
    send_data_to_graph(list_aggregation)


if __name__=="__main__":
    main()