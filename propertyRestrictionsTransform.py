import argparse
import json
import jsontools as jt
import sys


def transform_property_restrictions(data, key_to_transform):
    changed_any = False
    num_found = 0
    values, ignored = jt.find_key_context(key_to_transform, data, num_found)
    while values != {}:
        restrictions = values[key_to_transform]
        num_found += 1

        new_restrictions_list = []
        for restriction in restrictions:
            new_restrictions = {"Restrictions": []}

            for key, value in restriction.items():
                new_restrictions["Restrictions"].append("{0}:{1}".format(key, value))
                changed_any = True
            new_restrictions_list.append(new_restrictions)

        values[key_to_transform] = new_restrictions_list

        values, ignored = jt.find_key_context(key_to_transform, data, num_found)

    return changed_any


def process_campaign(file_path):
    # Get data from test files
    with open(file_path) as f:
        campaign_data = json.load(f)

    # Apply conversion rules
    changed_any1 = transform_property_restrictions(campaign_data, "Node_Property_Restrictions")
    changed_any2 = transform_property_restrictions(campaign_data, "Property_Restrictions_Within_Node")
    changed_any = changed_any1 or changed_any2


    # Write data back to json files
    if changed_any:
        with open(file_path, 'w') as f:
            json.dump(campaign_data, f, sort_keys=True, indent=4, separators=(',', ': '))


def process_collection(file_path):
    files = []
    # Read in the collection
    with open(file_path, "r") as file:
        for line in file:
            files.append(line.strip())

    # Search in every file listed
    for file in files:
        process_campaign(file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_path", help="Path to the JSON file for processing")
    parser.add_argument("--collection_path", help="Path to the file pointing to JSON files for processing")
    args = parser.parse_args()

    if args.file_path and args.collection_path or not args.file_path and not args.collection_path:
        print("Exactly one of file_path or collection_path must be specified")
        sys.exit(2)
    if args.file_path:
        process_campaign(args.file_path)
    elif args.collection_path:
        process_collection(args.collection_path)
