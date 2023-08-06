# -*- coding: utf-8 -*-
import csv

name = "guacamoleETL"
specified_columns = ['engine-location', 'num-of-cylinders', 'engine-size',
                     'weight', 'horsepower', 'aspiration', 'price', 'make']
output_columns = ['engine-location_front', 'engine-location_rear', 'num-of-cylinders',
                  'engine-size', 'weight', 'horsepower', 'aspiration_turbo', 'price', 'make']

units = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]
numwords = {}
for idx, word in enumerate(units):
    numwords[word] = idx


def transform(path):
    """Transform the data through given specifications into a matrix."""
    read_data = txt_data_to_cleaned_list(path)
    transformed_data = []
    transformed_data.append(output_columns)

    for this_record in read_data:
        transformed_row = []

        if this_record['engine-location'] == 'front':
            transformed_row.append(1)
        else:
            transformed_row.append(0)

        if this_record['engine-location'] == 'rear':
            transformed_row.append(1)
        else:
            transformed_row.append(0)

        transformed_row.append(numwords[this_record['num-of-cylinders']])

        transformed_row.append(int(this_record['engine-size']))

        transformed_row.append(int(this_record['weight']))

        transformed_row.append(float(this_record['horsepower'].replace(',', '.')))

        if this_record['aspiration'] == 'turbo':
            transformed_row.append(1)
        else:
            transformed_row.append(0)

        transformed_row.append(float(this_record['price'])/100)

        transformed_row.append(this_record['make'])

        transformed_data.append(transformed_row)

    return transformed_data


def load(path):
    """Load the data into a .csv file."""
    transformed_data = transform(path)
    with open('output.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(transformed_data)


def txt_data_to_cleaned_list(txt_file):
    """Data pre-process."""
    extract_data(txt_file)
    return clean_up()


def extract_data(txt_file):
    """Extract data from a .txt file to a temporary .csv file."""
    input_file = open(txt_file, 'r')
    temp_file = open('temp.csv', 'w', newline='')
    reader = csv.reader(input_file, delimiter=';')
    writer = csv.writer(temp_file)

    for row in reader:
        # pre-clean the data with leading or trailing whitespace
        writer.writerows([[x.strip() for x in row]])

    input_file.close()
    temp_file.close()


def clean_up():
    """Clean up the data with invalid information."""
    stream = open('temp.csv', 'r')
    data_list = list(csv.DictReader(stream))
    stream.close()

    clean_up_data = []
    for this_record in data_list:
        is_valid = 1

        for column in specified_columns:
            if this_record[column] == '-':
                is_valid = 0
                continue

        if is_valid == 1:
            clean_up_data.append(this_record)

    return clean_up_data
