import csv
import sqlite3
import datetime as dt
import os

from users.models import User

to_datetime = lambda date_string: dt.datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S.%fZ')

DB_NAME = "db.sqlite3"
FIELD_TYPES_BY_MODEL_NAME = {
    'category': {'id': int},
    'genre': {'id': int},
    'user': {'id': int},
    'title_genre': {'id': int, 'title_id': int, 'genre_id': int},
    'title': {'id': int, 'category_id': int, 'year': int},
    'review': {'id': int, 'title_id': int, 'author_id': int, 'score': int, 'pub_date': to_datetime},
    'comment': {'id': int, 'review_id': int, 'author_id': int, 'pub_date': to_datetime},
}

FILE_NAME_BY_MODEL_NAME = {
    'category': 'category.csv',
    'genre': 'genre.csv',
    'user': 'users.csv',
    'title_genre': 'genre_title.csv',
    'title': 'titles.csv',
    'review': 'review.csv',
    'comment': 'comments.csv',
}


def import_users():
    file_name = FILE_NAME_BY_MODEL_NAME['user']
    data_file = os.path.abspath(f'data/{file_name}')
    with open(data_file, 'r', encoding='utf-8') as f:
        dr = csv.DictReader(f, quoting=csv.QUOTE_MINIMAL)
        fieldnames = dr.fieldnames

        for row in dr:
            data = {}
            for name in fieldnames:
                convert_func = FIELD_TYPES_BY_MODEL_NAME['user'].get(name, str)
                data[name] = convert_func(row[name])

            User.objects.create_user(**data)


def import_data_from_csv_to_db(model_name):
    file_name = FILE_NAME_BY_MODEL_NAME[model_name]
    data_file = os.path.abspath(f'data/{file_name}')
    with open(data_file, 'r', encoding='utf-8') as f:
        dr = csv.DictReader(f, quoting=csv.QUOTE_MINIMAL)
        fieldnames = dr.fieldnames
        data = []
        for row in dr:
            row_data = []
            for name in fieldnames:
                convert_func = FIELD_TYPES_BY_MODEL_NAME[model_name].get(name, str)
                row_data.append(convert_func(row[name]))

            data.append(row_data)

    app_name = 'users' if model_name == 'user' else 'api'
    query = "INSERT INTO {}_{} ({}) VALUES ({});".format(
            app_name,
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


if __name__ == '__main__':
    import_users()
    for model_name in FIELD_TYPES_BY_MODEL_NAME.keys():
        if model_name == 'user':
            continue
        import_data_from_csv_to_db(model_name)
