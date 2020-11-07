import csv
import sqlite3
import os

DB_NAME = "db.sqlite3"
# with open(os.path.abspath(r'data/category.csv'), 'r', encoding='utf-8') as f:
#     dr = csv.DictReader(f)
#     for row in dr:
#         Category.objects.create(**row)


def import_data_from_csv_to_db(resource_name):
    data_file = os.path.abspath(f'data/{resource_name}.csv')
    with open(data_file, 'r', encoding='utf-8') as f:
        dr = csv.DictReader(f)
        fieldnames = dr.fieldnames
        data = [tuple(row.values()) for row in dr]

    query = "INSERT INTO api_{} ({}) VALUES ({});".format(
            resource_name,
            ','.join(fieldnames),
            ','.join(['?'] * len(fieldnames))
        )

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    try:
        cursor.executemany(query, data)
        connection.commit()
    except:
        print(f"Failed to import data {resource_name}")
    finally:
        connection.close()
