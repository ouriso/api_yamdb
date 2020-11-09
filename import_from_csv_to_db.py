import csv
import sqlite3
import os


DB_NAME = "db.sqlite3"
# with open(os.path.abspath(r'data/titles.csv'), 'r', encoding='utf-8') as f:
#     dr = csv.DictReader(f)
#     for row in dr:
#         Title.objects.create(**row)


def import_data_from_csv_to_db(file_name, model_name):
    data_file = os.path.abspath(f'data/{file_name}.csv')
    with open(data_file, 'r', encoding='utf-8') as f:
        dr = csv.DictReader(f, quoting=csv.QUOTE_MINIMAL)
        fieldnames = dr.fieldnames
        data = []
        for row in dr:
            row_data = []
            for name in fieldnames:
                if name.endswith('_id') or name == 'year':
                    val = int(row[name])
                else:
                    val = row[name]
                row_data.append(val)

            data.append(row_data)

    query = "INSERT INTO api_{} ({}) VALUES ({});".format(
            model_name,
            ','.join(fieldnames),
            ','.join(['?'] * len(fieldnames))
        )

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    try:
        cursor.executemany(query, data)
        connection.commit()
    except Exception as e:
        print(f"Failed to import data {model_name}: {e}")
    finally:
        connection.close()
