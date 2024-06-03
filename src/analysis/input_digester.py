import csv


def get_section_data(input_data_path: str, section_name: str) -> set[tuple]:
    data = set()
    with open(input_data_path, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        section_found = False
        for row in reader:
            if row[0] == section_name:
                section_found = True
                continue
            if section_found and not row[0].isdigit():
                break
            if section_found:
                row_data = tuple(int(value) for value in row if value)
                data.add(row_data)
    return data
