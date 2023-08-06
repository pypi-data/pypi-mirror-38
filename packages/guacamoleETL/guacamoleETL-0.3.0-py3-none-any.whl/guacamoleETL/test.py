# -*- coding: utf-8 -*-
from guacamoleETL.load import load
from guacamoleETL.transform import transform


if __name__ == "__main__":
    load()
    result = transform()
    print (result)
