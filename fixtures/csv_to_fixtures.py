#!/bin/python3
import csv
import json
import pathlib

from csv_to_fixtures_settings import FIXTURES_AFFILIATIONS, MANY_TO_MANY_FIELDS

CURRENT_DIR = pathlib.Path(__file__).parent.absolute()


def _convert_field_value_type(value: str):
    if value.isdigit():
        return int(value)
    if value.lower() in ["true", "false"]:
        return value.lower() == "true"

    return value


def converter(csv_filename, json_filename, app_model, many_to_many_fields=None):
    if many_to_many_fields is None:
        many_to_many_fields = {}
    with open(csv_filename, "rt", encoding="utf-8") as fin:
        csv_reader = csv.DictReader(fin)
        csv_reader.fieldnames = [field.lower() for field in csv_reader.fieldnames]
        json_list = [
            {
                "model": app_model,
                "id": _convert_field_value_type(row["id"]),
                "fields": {**{
                    key: _convert_field_value_type(value)
                    for key, value in row.items()
                    if key not in [
                        *(list(many_to_many_fields.keys()) if many_to_many_fields else []), "id",
                    ]
                }, **{
                    many_to_many_fields[key]: [_convert_field_value_type(value), ]
                    for key, value in row.items()
                    if key in many_to_many_fields
                }},
                # .update({
                #     many_to_many_fields[key]: [_convert_field_value_type(value), ]
                #     for key, value in row.items()
                #     if key in many_to_many_fields
                # }),
            } for row in csv_reader]

    with open(json_filename, "wt", encoding="utf-8") as fou:
        json.dump(json_list, fou, indent=4, ensure_ascii=False)


index = 0
for csv_name in CURRENT_DIR.glob("*.csv"):

    if csv_name.name not in FIXTURES_AFFILIATIONS:
        continue

    json_name = csv_name.with_suffix(".json")

    if json_name.exists():
        continue

    index += 1

    print(f"{index}) "
          f"{csv_name.relative_to(CURRENT_DIR.parent)} -> "
          f"{json_name.relative_to(CURRENT_DIR.parent)}")

    converter(
        csv_filename=csv_name,
        json_filename=json_name,
        app_model=FIXTURES_AFFILIATIONS[csv_name.name],
        many_to_many_fields=MANY_TO_MANY_FIELDS.get(csv_name.name)
    )
