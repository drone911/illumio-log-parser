from argparse import ArgumentParser

from utility.parse import parse_and_aggregate_flow_logs
from utility.inputs import generate_lookup_table, read_protocol_table
from utility.outputs import write_to_csv

# Default file names to write outputs to
DEFAULT_COUNT_FLOW_TAGS_FILE = "flow-tags-count.csv"
DEFAULT_COUNT_PORT_PROTOCOL_FILE = "port-protocol-count.csv"

# Path to protocols file that maps protocol number to it's name (src from AWS: http://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml)
PROTOCOL_FILE_PATH = "resource/protocol-numbers.csv"

FLOW_DEBUG_PRINT_INTERVAL = 5000


def main():
    parser = ArgumentParser()

    parser.add_argument("flow_logs_file_path",
                        help="Path to flow logs file to read from.", metavar="flow_logs_path")

    parser.add_argument("lookup_file_path",
                        help="Path to lookup file to aggregate logs.", metavar="lookup_path")

    parser.add_argument("-tc", "--tag-count-path", default=DEFAULT_COUNT_FLOW_TAGS_FILE,
                        help="Path to count of tags output file", metavar="tag_count_path")

    parser.add_argument("-pc", "--port-protocol-count-path", default=DEFAULT_COUNT_PORT_PROTOCOL_FILE,
                        help="Path to count of ports and protocols output file", metavar="port_protocol_count_path")

    args = parser.parse_args()

    print(f"[Debug] Reading and generating lookup table from file {args.lookup_file_path}...")
    lookup_table = generate_lookup_table(args.lookup_file_path)

    print(f"[Debug] Reading protocol number->name map table from file {PROTOCOL_FILE_PATH}...")
    protocol_table = read_protocol_table(PROTOCOL_FILE_PATH)

    print(f"[Debug] Parsing Logs from file {args.flow_logs_file_path}...")
    aggregates = parse_and_aggregate_flow_logs(
        args.flow_logs_file_path, lookup_table, protocol_table, FLOW_DEBUG_PRINT_INTERVAL)

    print(f"[Debug] Writing counted tags to file {args.tag_count_path}...")
    write_to_csv(args.tag_count_path,
                ["Tag", "Count"], aggregates["count_tags"])

    print(f"[Debug] Writing counted ports and protocols to file {args.port_protocol_count_path}")
    write_to_csv(args.port_protocol_count_path, 
                ["Port", "Protocol", "Count"], aggregates["count_port_and_protocol"])


if __name__ == "__main__":
    main()
