import os
import uuid
from argparse import ArgumentParser


class FileAdapter:

    @staticmethod
    def read_csv(file_path):
        import csv
        with open(file_path, encoding='utf-8-sig') as f:
            reader = csv.reader(f, delimiter=",", quotechar='"')
            return [x for x in reader]

    @staticmethod
    def read_xlsx():
        pass

    @staticmethod
    def save_json(data, filename):
        import json
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)


def build_control(data_line):
    return {
        "id": data_line[0],
        "class": "family",
        "title": data_line[1],
        "parameters": [],
        "properties": [
            {
                "name": "label",
                "value": data_line[0].upper()
            },
            {
                "name": "sort-id",
                "value": data_line[0].lower()
            }
        ],
        "links": [
            {
                "href": "#ref050",
                "rel": "reference",
                "text": "NIST Special Publication 800-171"
            },
        ],
        "parts": [
            {
                "id": f"{data_line[0]}_discussion",
                "name": "discussion",
                "prose": data_line[2],
                "links": []
            },
        ]
    }


def generate_metadata():
    # todo - extract later
    return {
        "title": "Protecting Controlled Unclassified Information in Nonfederal Systems and Organizations",
        "last-modified": "2020-02-04T14:55:16.051-05:00",
        "version": "2015-01-22",
        "oscal-version": "1.0.0-milestone3",
        "properties": [],
        "links": [],
        "roles": [],
        "parties": [],
        "responsible-parties": {},
    }


def get_groups():
    # todo - extract later
    return [
               {
                   "id": "ac",
                   "class": "family",
                   "title": "Access Control",
                   "controls": []
               },
           ]


def fresh_mapping():
    # https://github.com/usnistgov/OSCAL/blob/93ef403b9f79ebf9f5ea01195bbab9bca45cd5bd/json/schema/oscal_catalog_schema.json

    return {
        "catalog": {
            "id": uuid.uuid4().hex,
            "metadata": generate_metadata(),
            "groups": get_groups(),
            "controls": {},
            "back-matter": {}
        }
    }


if __name__ == "__main__":
    parser = ArgumentParser(description="NIST_SP-800-53")
    parser.add_argument("-i", dest="filename", required=True,
                        help="filename for csv", metavar="FILE")
    parser.add_argument("-o", dest="output", required=True,
                        help="output filename for json", metavar="FILE")
    args = parser.parse_args()
    mapping = fresh_mapping()

    if not os.path.exists(args.filename):
        raise Exception(f"{args.filename} does not exist.  Check the path of the file and try again.")

    for line in FileAdapter.read_csv(args.filename):
        mapping['catalog']['groups'][0]['controls'].append(build_control(line))
    FileAdapter.save_json(mapping, args.output)
