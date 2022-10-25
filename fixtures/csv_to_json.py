#!/bin/python3
import csv
import json
import pathlib

from csv_to_json_settings import FIXTURES_AFFILIATION

CURRENT_DIR = pathlib.Path(__file__).parent.absolute()


def converter(csv_filename, json_filename):
    with open(csv_filename, "rt", encoding="utf-8") as fin:
        csv_reader = csv.DictReader(fin)
        json_list = [row for row in csv_reader]
    with open(json_filename, "wt", encoding="utf-8") as fou:
        json.dump(json_list, fou, indent=4, ensure_ascii=False)


index = 0
for csv_name in CURRENT_DIR.glob("*.csv"):
    if csv_name.name in FIXTURES_AFFILIATION:
        json_name = CURRENT_DIR.parent / FIXTURES_AFFILIATION[csv_name.name] / \
                    ("fixtures/" + csv_name.stem + ".json")
        json_name.parent.mkdir(parents=True, exist_ok=True)
    else:
        json_name = csv_name.with_suffix(".json")

    index += 1
    print(f"{index}) "
          f"{csv_name.relative_to(CURRENT_DIR.parent)} -> "
          f"{json_name.relative_to(CURRENT_DIR.parent)}")
    converter(
        csv_filename=csv_name,
        json_filename=json_name,
    )
