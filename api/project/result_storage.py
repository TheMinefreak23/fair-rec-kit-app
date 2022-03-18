# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
import csv  # TODO fix this import
from csv import writer
import time

# Result format
# group ID
# metadata: timestamp, name, tag
# settings: dataset, approach, metrics
# result: ranking, metrics results

current_result = {}


def save_result(metadata,settings,result):
    timestamp = time.time()
    global current_result # TODO use class instead of global?
    metadata[timestamp] = timestamp
    # use timestamp as group_id for now
    current_result = [timestamp,metadata,settings,result]
    add_csv_row(current_result, 'results.tsv')


def newest_result():
    return current_result


def load_results():
    #path = 'test_results/magic_mock.tsv'
    path = 'results.tsv'
    return list_from_csv(path)


def add_csv_row(row_list, path):
    # Open our existing CSV file in append mode
    # Create a file object and write a row to it
    with open(path, 'a') as file:
        file_writer = writer(file)
        file_writer.writerow(row_list)
        file.close()


def list_from_csv(path):
    with open(path, mode='r') as file:
        reader = csv.reader(file)
        rows = list(reader)
        return rows
