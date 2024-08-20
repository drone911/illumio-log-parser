import csv


def generate_lookup_table(file_path):
    """
        From a lookup tags file, create a lookup table.
    """
    lookup_table = {}

    with open(file_path, "r", newline='') as lookup_fp:
        lookup_reader = csv.reader(lookup_fp)

        # Skip the header
        next(lookup_reader, None)
        for idx, lookup_line in enumerate(lookup_reader):
            if not lookup_line:
                continue
            assert len(
                lookup_line) == 3, f"[Incorrect Format] Lookup table row {idx+1} does not have 3 columns: {lookup_line}"

            # Get destination port, protocl, and tag
            dst_port = lookup_line[0].lower().strip()
            protocol = lookup_line[1].lower().strip()
            tag = lookup_line[2].strip()

            # Use destination port as primary key
            lookup_table[dst_port] = {
                # Get already store record
                **lookup_table.get(dst_port, {}),
                # Use protocol as secondary key and value as the tag
                protocol: tag
            }

    return lookup_table


def read_protocol_table(file_path):
    """
        From IANA protocols file, create a protocol lookup table.
    """
    protocol_table = {}

    with open(file_path, "r", newline='') as protocol_fp:
        protocol_reader = csv.reader(protocol_fp)
        # Skip the header
        next(protocol_reader, None)
        for idx, protocol_line in enumerate(protocol_reader):
            if not protocol_line:
                continue
            protocol_table[protocol_line[0]] = protocol_line[1].lower()

    return protocol_table
