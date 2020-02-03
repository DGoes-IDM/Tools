
def add_param(file_data, key, value):
    file_data["parameters"][key] = value


def add_to_files_in_collection(file_path, key, value, ignore_missing):
    files = []
    # Read in the collection
    with open(file_path, "r") as file:
        for line in file:
            files.append(line.strip())

    # Replace chunks in every file listed
    for file in files:
        add_to_file(file, key, value, ignore_missing)


def add_to_file(file_path, key, value, ignore_missing):
    # Get data from json file
    try:
        with open(file_path) as file:
            file_data = json.load(file)
    except Exception as e:
        if ignore_missing:
            return
        else:
            raise e

    # Fix up json file
    add_param(file_data, key, value)

    # Write data back to json file
    with open(file_path, 'w') as f:
        json.dump(file_data, f, sort_keys=True, indent=4, separators=(',', ': '))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_path", help="Path to the JSON file for addition")
    parser.add_argument("--collection_path", help="Path to the file pointing to JSON files for addition")
    parser.add_argument("key", help="Name of the parameter key to add")
    parser.add_argument("value", help="Value to set the new parameter to")
    parser.add_argument("--ignore_missing", action='store_true', help="Ignore any files that can't be found")
    args = parser.parse_args()

    if args.file_path and args.collection_path or not args.file_path and not args.collection_path:
        print("Exactly one of file_path or collection_path must be specified")
        sys.exit(2)
    if args.file_path:
        add_to_file(args.file_path, args.key, args.value, args.ignore_missing)
    elif args.collection_path:
        add_to_files_in_collection(args.collection_path, args.key, args.value, args.ignore_missing)
