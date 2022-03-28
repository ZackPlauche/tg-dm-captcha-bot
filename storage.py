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
                result.append(row)
    except:
        with open("ban_list.csv", "w") as e: pass

    return result


def get_user(chat_id):
    for row in get_ban_list():
        if str(chat_id).strip() == row[0].strip():
            return {
                "chat_id": row[0].strip(),
                "timestamp": row[1].strip(),
            }

    return None


def rm_from_ban_list(chat_id):
    with open('ban_list.csv', 'w', newline='') as outcsv:
        writer = csv.writer(outcsv)
        for row in get_ban_list():
            if str(chat_id).strip() not in row: writer.writerow(row)