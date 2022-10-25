#!/bin/python3
import csv
import json
import pathlib


FIXTURES_DIR =


def converter(csv_filename, json_filename):
    with open(csv_filename, "rt", encoding="utf-8") as fin:
        csv_reader = csv.DictReader(fin)
        for row in csv_reader:
            print(row)





