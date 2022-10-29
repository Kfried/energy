from aggregation_control import *
from chart_manager import Chart
import pandas

import bson

import api_handler
from Mongo import *
from data import *
from EnergyRecord import EnergyRecord
from api_handler import get_data


def parse_file(file_name):
    with open(file_name, "r") as file:
        file_content = file.readlines()
    if 'kWh' in file_content[0]:
        collection_name = 'electricity'
    else:
        collection_name = "gas"

    parsed_data = []

    for iterate_count in range(1, len(file_content)):
        print(iterate_count)
        record = EnergyRecord(data_line=file_content[iterate_count], source_type=collection_name)
        parsed_data.append(record.record_as_dict())
    print(parsed_data)
    return parsed_data


def parse_records_to_json(records):
    parsed_data = []
    for record in records:
        parsed_data.append(record.record_as_dict())
    return parsed_data


def write_to_mongo(db, content, collection):
    db.initialise_db(collection)
    db.insert_data(collection, content)


def read_from_mongo(db, collection, source_type):
    db.initialise_db(collection)
    filter = {'source_type': source_type}
    return db.get_data(collection, filter)


def connect(database_name):
    return mongo_db(connection_string, password, database_name)


def load_from_file(databse, collection, file_name):
    data_to_load = parse_file(file_name)
    write_to_mongo(databse, data_to_load, collection)


def get_last_record(dataset):
    return dataset[-1]


def send_data_to_graph(data):
    contents = None
    with open("data_graph.html", "r") as in_file, open("data_graph_populated.html", "w") as out_file:
        contents = in_file.read()
        contents = contents.replace("xxnumberpointsxx", f"{len(data)}")
        contents = contents.replace("xxdataxx", str(data))
        out_file.write(contents)


def format_dates(line):
    delimit = line.split(',')
    date_range = f'?period_from={delimit[0]}T00:00Z&period_to={delimit[1]}T00:00Z'
    return date_range


def main():
    loaded = False
    arguments = {}
    db = connect('energy')
    active_commands = ['loadcsv', 'view', 'sync', 'load', 'exit', 'render', 'loadeddates']
    records = []
    while True:
        command = input(">")
        delimited = command.split()

        if len(delimited) == 0:
            return param_error(active_commands, "No command supplied")
        else:
            command = delimited[0].lower()
            arg_list = delimited[1:]
            for item in arg_list:
                try:
                    delimit_argument = item.split('=')
                    arguments[delimit_argument[0]] = delimit_argument[1]
                except:
                    print('There was a problem parsing arguments')
                    return 0

        if command not in active_commands:
            return param_error(active_commands, "Command not recognised")

        if command == 'load':
            if arguments['type'] == 'csv':
                load_from_file(db, arguments['type'], arguments['source'])
            elif arguments['type'] == 'api':
                if 'dates' in arguments:
                    data = api_handler.get_data(arguments['source'], dates=format_dates(arguments['dates']))
                else:
                    data = api_handler.get_data(arguments['source'])
                for reading_set in data:
                    for reading in reading_set:
                        records.append(EnergyRecord(api_entry=reading, source_type=arguments['source']))
                if 'agg' in arguments:
                    aggregation = aggregate_data(records, arguments['agg'])
                    records = aggregation
                for r in records:
                    print(r)
            loaded = True

        if command == 'render':
            if loaded:
                source_type = arguments['source']
                chart = Chart('line', source_type, records)
                chart.update_page('chart.html', 'chart_rendered.html')

        if command == 'view':
            content = get_data(arguments['type'])
            for item in content.items():
                print(item)

        #sync logic
        '''
        This logic is the heavyweight:
        given records for a collection are loaded to memory 
        when the sync is executed
        then the records are loaded to the appropriate collection 
            AND duplicate timestamps overwrite target
            AND runner collection is updated for collection start and end'''
        if command == 'sync':
            if loaded:
                collection_name = arguments['collection']
                check_collection = db.check_collection_present(collection_name)
                if check_collection:
                    #collection present logic
                    print('collection available')
                    if 'wipe' in arguments:
                        if db.drop_collection(collection_name):
                            print('collection purged, reloading')
                    db.insert_data(collection_name, parse_records_to_json(records))

                else:
                    add_it = input(f'collection {collection_name} is not available, do you want to add it')
                    if add_it:
                        if db.create_collection(collection_name):
                            db.insert_data(collection_name, parse_records_to_json(records))
                    else:
                        print('exiting sync')

        if command == 'aggregagte':
            if loaded:
                records = aggregate_data(records, arguments['value'])
            else:
                print('no data loaded')

        #update logic

        if command == 'exit':
            return

    return

    collection_name = "energy"

    # load_from_file(db,"energy", "../electricity.csv")
    # load_from_file(db,"energy","../gas.csv")

    data = read_from_mongo(db, collection_name, {'source_type': 'electricity'})
    record_collection = []
    for rec in data:
        record_collection.append(EnergyRecord(rec))
    last_record = get_last_record(record_collection)

    aggregated_data = aggregate_by_day(record_collection)
    list_aggregation = list(aggregated_data.values())
    max_value = max(list_aggregation)
    min_value = min(list_aggregation)
    print(max_value, min_value)
    # send_data_to_graph(list_aggregation)


def param_error(active_commands, message):
    print(message)
    print("currently available commands:")
    for c in active_commands:
        print(c)
    return (0)


if __name__ == "__main__":
    main()

# update view to bring data to array
