import csv
import sqlite3
import datetime as dt
import os

from functools import partial

to_datetime = partial(dt.datetime.strptime, format='%Y-%m-%dT%H:%M:%S.%fZ')

DB_NAME = "db.sqlite3"
FIELD_TYPES = {
    'users': {'id': int},
    'titles': {'id': int, 'category_id': int, 'year': int},
    'review': {'id': int, 'title_id': int, 'author_id': int, 'score': int, 'pub_date': to_datetime}
}


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
