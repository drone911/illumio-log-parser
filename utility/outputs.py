import csv


def write_count_tags(file_path, count_tags):
    """
        Write the counted tags to the specified file in csv format.
    """
    with open(file_path, 'w', newline='') as count_tags_fp:
        count_tags_writer = csv.writer(count_tags_fp)

        count_tags_writer.writerow(["Tag", "Count"])

        for tag, tag_count in count_tags.items():
            count_tags_writer.writerow([tag, tag_count])


def write_count_port_protocol(file_path, count_port_and_protocol):
    """
        Write the counted ports and protocols to the specified file in csv format.
    """
    with open(file_path, 'w', newline='') as count_port_and_protocol_fp:
        count_port_and_protocol_writer = csv.writer(count_port_and_protocol_fp)

        count_port_and_protocol_writer.writerow(["Port", "Protocol", "Count"])

        for port, protocol_counts in count_port_and_protocol.items():
            for protocol, count in protocol_counts.items():
                count_port_and_protocol_writer.writerow(
                    [port, protocol, count])
