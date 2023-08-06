# -*- coding: utf-8 -*-
import csv

columns = ['engine-location', 'num-of-cylinders', 'engine-size', ]


def txt_datareader(txt_file):
    input_file = open(txt_file, 'r')
    temp_file = open('./guacamoleETL/raw_data/temp.csv', 'w', newline='')
    reader = csv.reader(input_file, delimiter=';')
    writer = csv.writer(temp_file)

    for row in reader:
        writer.writerows([[x.strip() for x in row]])

    input_file.close()
    temp_file.close()

    stream = open('./guacamoleETL/raw_data/temp.csv', 'r')
    data_list = list(csv.DictReader(stream))
    stream.close()

    clean_date = []
    # for each_record in data_list:

    return data_list
