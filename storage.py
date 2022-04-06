import csv
from pathlib import Path

ban_list_csv = Path('ban_list.csv')

if not ban_list_csv.exists():
    ban_list_csv.touch()


def write_row_to_ban_list(data):
    with ban_list_csv.open('a', newline='') as outcsv:
        writer = csv.writer(outcsv)
        writer.writerow(data)


def get_ban_list():
    result = []
    with ban_list_csv.open(newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        result.extend([row for row in csv_reader if int(row[4]) == 0])
    return result


def get_csv_users():
    result = []
    with ban_list_csv.open(newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        for row in csv_reader:
            result.append(row)
    return result


def get_user(chat_id):
    for row in get_csv_users():
        if str(chat_id).strip() == row[0].strip():
            return {
                "chat_id": row[0].strip(),
                "timestamp": row[1].strip(),
                "name": row[2].strip(),
                "code": row[3].strip(),
                "status": row[4].strip()
            }
    return None


def rm_from_ban_list(chat_id):
    with ban_list_csv.open('w', newline='') as outcsv:
        writer = csv.writer(outcsv)
        for row in get_csv_users():
            if str(chat_id).strip() not in row: 
                writer.writerow(row)


def update_user_code(chat_id, code):
    rows = get_csv_users()
    with ban_list_csv.open('w', newline='') as outcsv:
        writer = csv.writer(outcsv)
        for row in rows:
            if str(chat_id).strip() in row:
                row[3] = str(code).strip()
            writer.writerow(row)


def update_user_status(chat_id, status):
    rows = get_csv_users()
    with ban_list_csv.open('w', newline='') as outcsv:
        writer = csv.writer(outcsv)
        for row in rows:
            if str(chat_id).strip() in row:
                row[4] = str(status).strip()
            writer.writerow(row)