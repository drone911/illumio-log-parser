import csv


def write_to_csv(file_path, headers, csv_data):
    """
        Write data to csv with provided headers. If the data values contains dictionary, write it recursively too.
    """
    with open(file_path, 'w', newline='') as csv_fp:
        csv_writer = csv.writer(csv_fp)

        csv_writer.writerow(headers)

        for key, value in csv_data.items():
            if type(value) == dict:
                for nested_key, nested_value in value.items():
                    csv_writer.writerow(
                        [key, nested_key, nested_value])
            else:
                csv_writer.writerow([key, value])
