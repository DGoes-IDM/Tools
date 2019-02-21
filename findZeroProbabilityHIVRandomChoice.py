import sys
import json
import argparse
import jsontools as jt
import os


def search_json(data):
    erased_any = False
    num_found = 0
    values, ignored = jt.find_key_context("Choice_Probabilities", data, num_found)
    while values != {}:
        num_found += 1
        while 0 in values["Choice_Probabilities"]:
            index = values["Choice_Probabilities"].index(0)
            del values["Choice_Probabilities"][index]
            del values["Choice_Names"][index]
            erased_any = True

        values, ignored = jt.find_key_context("Choice_Probabilities", data, num_found)

    return erased_any


def find_in_file(file_path):
    # Get data from json file
    try:
        with open(file_path) as file:
            file_data = json.load(file)
    except Exception as e:
        raise e

    # Dig through json file
    erased_any = search_json(file_data, os.path.normpath(file_path))

    # Write data back to json file, if we changed anything
    if erased_any:
        with open(file_path, 'w') as f:
            json.dump(file_data, f, sort_keys=True, indent=4, separators=(',', ': '))


def find_in_collection(file_path):
    files = []
    # Read in the collection
    with open(file_path, "r") as file:
        for line in file:
            files.append(line.strip())

    # Search in every file listed
    for file in files:
        find_in_file(file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_path", help="Path to the JSON file for searching")
    parser.add_argument("--collection_path", help="Path to the file pointing to JSON files for searching")
    args = parser.parse_args()

    if args.file_path and args.collection_path or not args.file_path and not args.collection_path:
        print("Exactly one of file_path or collection_path must be specified")
        sys.exit(2)
    if args.file_path:
        find_in_file(args.file_path)
    elif args.collection_path:
        find_in_collection(args.collection_path)
