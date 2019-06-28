import argparse
import json
import csv
import os


def create_patient_output(data, output_directory):
    # Open CSV for writing
    filename = "{0}\patient_{1}.csv".format(output_directory, data["id"])
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        for channel_name, channel in data.items():
            channel = channel if isinstance(channel, list) else [channel]
            channel = channel[0] if isinstance(channel[0], list) else channel
            writer.writerow([channel_name] + channel)


def process_patient_report(file_path, output_directory):
    # Get data from json file
    with open(file_path) as file:
        file_data = json.load(file)

    # Correct output directory if none was provided
    if output_directory == "":
        output_directory = os.path.dirname(file_path)

    # For each patient...
    for patient in file_data["patient_array"]:
        # Create a patient data file
        create_patient_output(patient, output_directory)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", help="Path to the malaria patient report JSON file")
    parser.add_argument("--output-directory", default="", help="Optional path to the output directory to emit "
                                                                   "CSV files")
    args = parser.parse_args()

    process_patient_report(args.file_path, args.output_directory)