# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
import csv  # TODO fix this import
from csv import writer
import time
import pandas as pd
from flask import (Blueprint, request)

results_bp = Blueprint('results', __name__, url_prefix='/all-results')

# Temporary list with results of calculations
results = [
    {
        'timestamp': '0',
        'number': '0',
        'reverse': ''
    }
]


@results_bp.route('/results', methods=['GET'])
def results():
    return load_results()


def save_result(number, reverse):
    timestamp = time.time()
    add_csv_row([timestamp, number, reverse], 'results.tsv')


def load_results():
    #path = 'test_results/magic_mock.tsv'
    path = 'results.tsv'
    return list_from_csv(path)


def add_csv_row(row_list, path):
    # Open our existing CSV file in append mode
    # Create a file object and write a row to it
    with open(path, 'a') as file:
        file_writer = writer(file)
        file_writer.writerow(list)
        file.close()


def list_from_csv(path):
    with open(path, mode='r') as file:
        reader = csv.reader(file)
        rows = list(reader)
        return rows
