import csv


def write_row_to_ban_list(data):
    with open('ban_list.csv', 'a', newline='') as outcsv:
        writer = csv.writer(outcsv)
        writer.writerow(data)


def get_ban_list():
    result = []
    try:
        with open('ban_list.csv', newline='') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=',')
            for row in csv_reader:
                if int(row[4]) == 0: result.append(row)
    except:
        with open("ban_list.csv", "w") as e: pass

    return result


def get_csv_users():
    result = []
    try:
        with open('ban_list.csv', newline='') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=',')
            for row in csv_reader:
                result.append(row)
    except:
        with open("ban_list.csv", "w") as e: pass

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
    with open('ban_list.csv', 'w', newline='') as outcsv:
        writer = csv.writer(outcsv)
        for row in get_csv_users():
            if str(chat_id).strip() not in row: writer.writerow(row)


def update_user_code(chat_id, code):
    rows = get_csv_users()
    with open('ban_list.csv', 'w', newline='') as outcsv:
        writer = csv.writer(outcsv)
        for row in rows:
            if str(chat_id).strip() in row:
                row[3] = str(code).strip()
            writer.writerow(row)


def update_user_status(chat_id, status):
    rows = get_csv_users()
    with open('ban_list.csv', 'w', newline='') as outcsv:
        writer = csv.writer(outcsv)
        for row in rows:
            if str(chat_id).strip() in row:
                row[4] = str(status).strip()
            writer.writerow(row)