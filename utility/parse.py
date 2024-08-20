def parse_and_aggregate_flow_logs(flow_logs_file_path, lookup_table, protocol_table, flow_debug_print_interval=5000):
    """
        Find count of tags and ports & protocols from flow logs.
    """
    idx_to_value_mapper = {
        6: "dst_port",
        7: "protocol"
    }

    def parse_flow_log(index, flow_log):
        """
            Get destination port and protocol from a single log
        """
        # We nest this function for better performance by removing the need to pass protocol_table and idx_to_value_mapper
        # on every function call

        flow_log = flow_log.split()
        assert len(
            flow_log) == 14, f"[Incorrect Format] Flow Log row {index+1} does not have 14 columns: {flow_log}"

        parsed_flow_log = {
            value_type: flow_log[idx].strip() for idx, value_type in idx_to_value_mapper.items()
        }
        return parsed_flow_log

    aggregates = {
        "count_tags": {},
        "count_port_and_protocol": {}
    }

    with open(flow_logs_file_path, "r", newline='') as flow_logs_fp:
        for idx, flow_log in enumerate(flow_logs_fp):
            if (idx + 1) % flow_debug_print_interval == 0:
                print(f"[Debug] Processed {idx + 1} logs")

            # remove spaces on both sides
            flow_log = flow_log.strip()
            if not flow_log:
                continue

            parsed_flow_log = parse_flow_log(idx, flow_log)

            protocol = protocol_table[parsed_flow_log["protocol"]]
            dst_port = parsed_flow_log["dst_port"]

            # Lookup tag from lookup table, and if not found, mark Untagged
            tag = lookup_table.get(dst_port.lower(), {}).get(
                protocol.lower(), "Untagged")

            # Count tags
            aggregates["count_tags"][tag] = 1 + \
                aggregates["count_tags"].get(tag, 0)

            # Count port and protocol
            count_port = aggregates["count_port_and_protocol"].get(
                dst_port, {})
            count_port[protocol] = 1 + count_port.get(protocol, 0)
            aggregates["count_port_and_protocol"][dst_port] = count_port

    return aggregates
