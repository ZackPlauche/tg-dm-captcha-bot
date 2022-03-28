import csv
from pathlib import Path

csv_file = Path('ban_list.csv')

if not csv_file.exists():
    csv_file.touch()


def write_row_to_ban_list(data):
    with csv_file.open('a', newline='') as outcsv:
        writer = csv.writer(outcsv)
        writer.writerow(data)


def get_ban_list():
    result = []
    with csv_file.open(newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        for row in csv_reader:
            result.append(row)
    return result


def rm_from_ban_list(chat_id):
    with csv_file.open('w', newline='') as outcsv:
        writer = csv.writer(outcsv)
        for row in get_ban_list():
            if str(chat_id).strip() not in row:
                writer.writerow(row)