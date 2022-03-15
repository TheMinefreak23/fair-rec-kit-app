# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
import csv # TODO fix this import
from csv import writer
import time
import pandas as pd
from flask import (Blueprint, request)

results_bp = Blueprint('results', __name__, url_prefix='/all-results')

# Temporary list with results of calculations
 calculations = [
    {
        'timestamp': '0',
        'number': '0',
        'reverse': ''
    }
 ]

MAX_TEMP = 100
#results_df = pd.DataFrame()


@results_bp.route('/results', methods=['GET', 'POST'])
def results():
    #return results_df.to_dict('index')


def save_result(number, reverse):
    timestamp = time.time()
    add_csv_row([timestamp,number,reverse])
    pd.read_csv()


def newest_result():
    #return results_df.tail(1)


def load_results():
    df = pd.read_csv('test_results/magic_mock.tsv').tail(MAX_TEMP)
    results = df.to_dict()
    #global results_df  # TODO class instead of global
    #results_df = df.tail(MAX_TEMP)
    #print(results_df)

def add_csv_row(list):
    # Open our existing CSV file in append mode
    # Create a file object and write a row to it
    with open('event.csv', 'a') as file:
        file_writer = writer(file)
        file_writer.writerow(list)
        file.close()

def dict_from_csv():
    with open('csv_file.csv', mode='r') as file:
        reader = csv.reader(file)
        return {rows[0]: rows[1] for rows in reader}