# -*- coding: utf-8 -*-
from guacamoleETL.tool import txt_datareader


def load(path):
    read_data = txt_datareader(path)
    print(read_data)
