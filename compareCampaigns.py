import argparse
import json

# TODO: create mode where the path through events is compared/drawn in ascii?


def compare_parsed_json(source, compared, source_context, result):
    printed_context = False
    for x in source:
        if type(source[x]) is not dict:
            if x not in compared:
                if not printed_context:
                    result += '\t{0}:\n'.format(source_context)
                    printed_context = True
                    result += '\t\t"{0}" is in first campaign and not second\n'.format(x)
            elif source[x] != compared[x]:
                if not printed_context:
                    result += '\t{0}:\n'.format(source_context)
                    printed_context = True
                result += '\t\t"{0}": {1} != {2}\n'.format(x, source[x], compared[x])
        else:
            if x not in compared:
                if not printed_context:
                    result += '\t{0}:\n'.format(source_context)
                    printed_context = True
                result += '\t\t"{0}" is in first campaign and not second\n'.format(x)
            else:
                result = compare_parsed_json(source[x], compared[x], '{0}: {1}'.format(source_context, x), result)
    return result


def compare_events(event1, event2, event_name):
    base_string = 'Event "{0}" common to both campaigns discovered! Comparing...\n'.format(event_name)
    result = compare_parsed_json(event1, event2, event_name, base_string)
    if result != base_string:
        print(result)


def get_event_with_name(events, name, context):
    result = None

    for event in events:
        if event["Event_Name"] == name:
            if result is not None:
                print('Warning: found multiple events with the same name in event list for {0}: "{1}"'.format(context,
                                                                                                              name))
            result = event

    return result


def compare_campaigns(campaign1, campaign2):
    events1 = campaign1["Events"]
    events2 = campaign2["Events"]

    # For each event in the first campaign...
    for event in events1:

        # Find that event in the second campaign
        event_name = event["Event_Name"]
        other_event = get_event_with_name(events2, event_name, 'second campaign')

        # If it doesn't exist, indicate the difference
        if other_event is None:
            print('Event in first campaign not found in second campaign: "{0}"'.format(event_name))
            print()

        # If it does exist, compare the events
        else:
            compare_events(event, other_event, event_name)

    # For each event in the second campaign...
    for event in events2:

        # Find that event in the first campaign
        event_name = event["Event_Name"]
        other_event = get_event_with_name(events1, event_name, 'first campaign')

        # If it doesn't exist, indicate the difference
        if other_event is None:
            print('Event in second campaign not found in first campaign: "{0}"'.format(event_name))
            print()


def compare_campaign_files(campaign1, campaign2):
    with open(campaign1) as c_file1, open(campaign2) as c_file2:
        c_data1 = json.load(c_file1)
        c_data2 = json.load(c_file2)

    compare_campaigns(c_data1, c_data2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("campaign1", help="Path to the first campaign file for comparison")
    parser.add_argument("campaign2", help="Path to the second campaign file for comparison")
    args = parser.parse_args()

    compare_campaign_files(args.campaign1, args.campaign2)