from utility.inputs import generate_lookup_table, read_protocol_table
from utility.parse import parse_and_aggregate_flow_logs
from utility.outputs import write_to_csv

import csv
import random
from datetime import datetime


def generate_test_flow_logs_file(record_count, flow_logs_path):
    with open(flow_logs_path, 'w') as flow_logs_fp:
        for _ in range(record_count):
            flow_logs_fp.write(
                f"2 123456789012 eni-0a1b2c3d 10.0.1.201 198.51.100.2 443 {random.randint(0, 65535)} {random.randint(0, 145)} 25 20000 1620140761 1620140821 ACCEPT OK\n")


def generate_test_lookup_file(record_count, lookup_path, protocols):
    with open(lookup_path, 'w', newline='') as lookup_fp:
        lookup_writer = csv.writer(lookup_fp)
        lookup_writer.writerow(["dstport", "protocol", "tag"])

        for _ in range(record_count):
            lookup_writer.writerow([random.randint(0, 65535), random.choice(
                protocols), f"tag-{random.randint(0, 65535)}"])


def test():
    """
        Test and profile the aggregate function for flow logs
    """

    current_timestamp = datetime.now()
    print(f"[Debug] Started test at {current_timestamp}")
    LOOKUP_RECORDS_TO_GENERATE = 10000
    # Close to 10 MB of logs
    FLOW_LOGS_TO_GENERATE = 100000

    LOOKUP_FILE_CREATION_PATH = f"test-outputs/lookup-test-{current_timestamp.strftime('%Y-%m-%d-%H-%M-%S')}.csv"
    FLOW_LOGS_FILE_CREATION_PATH = f"test-outputs/logs-test-{current_timestamp.strftime('%Y-%m-%d-%H-%M-%S')}.txt"
    PROTOCOL_FILE_PATH = "resource/protocol-numbers.csv"

    COUNT_TAGS_CREATION_PATH = f"test-outputs/count-tags-output-{current_timestamp.strftime('%Y-%m-%d-%H-%M-%S')}.txt"
    COUNT_PROTOCOL_PORT_PATH = f"test-outputs/count-port-protocol-output-{current_timestamp.strftime('%Y-%m-%d-%H-%M-%S')}.txt"

    protocol_table = read_protocol_table(PROTOCOL_FILE_PATH)

    print(f"[Debug] Generating lookup table...")
    # Generate lookup file and then read from it
    generate_test_lookup_file(LOOKUP_RECORDS_TO_GENERATE, LOOKUP_FILE_CREATION_PATH,
                              list(protocol_table.values()))
    lookup_table = generate_lookup_table(LOOKUP_FILE_CREATION_PATH)

    print(f"[Debug] Generating flow logs...")
    # Generate flow logs
    generate_test_flow_logs_file(FLOW_LOGS_TO_GENERATE,
                                 FLOW_LOGS_FILE_CREATION_PATH)

    # Note aggregation start time
    aggregate_start_time = datetime.now()
    print(f"[Debug] Started aggregating at {aggregate_start_time}...")

    # Aggregate logs
    aggregates = parse_and_aggregate_flow_logs(
        FLOW_LOGS_FILE_CREATION_PATH, lookup_table, protocol_table, FLOW_LOGS_TO_GENERATE//10)

    # Note aggregation end time
    aggregate_end_time = datetime.now()
    print(f"[Debug] Ended aggregating at {aggregate_end_time}...")

    print(
        f"[Debug] Writing counted tags to file {COUNT_TAGS_CREATION_PATH}...")
    write_to_csv(COUNT_TAGS_CREATION_PATH,
                ["Tag", "Count"], aggregates["count_tags"])

    print(f"[Debug] Writing counted ports and protocols to file {COUNT_PROTOCOL_PORT_PATH}")
    write_to_csv(COUNT_PROTOCOL_PORT_PATH,
                ["Port", "Protocol", "Count"], aggregates["count_port_and_protocol"])

    print(f"\nTime taken to aggregate {FLOW_LOGS_TO_GENERATE} flow records with {LOOKUP_RECORDS_TO_GENERATE} lookup records: {aggregate_end_time - aggregate_start_time}")


if __name__ == "__main__":
    test()
