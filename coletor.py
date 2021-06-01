
import requests
import json
import settings
import database_manager

db_file = settings.db_file

sql_create_breeds_table = settings.sql_create_breeds_table

conn = database_manager.create_connection(db_file)
database_manager.create_table(conn, sql_create_breeds_table)

url = settings.cats_api_url

headers = {
  'x-api-key': settings.cats_api_key
}

response = requests.get(url, headers=headers, verify=False)

cats = json.loads(response.text)

cats_list = []

for cat in cats:
    record = (cat['id'], cat['name'], cat['temperament'], cat['origin'], cat['description'])

    cats_list.append(record)

print(cats_list)

rowcount = database_manager.insert_cats_breeds(conn, cats_list)

print(rowcount)

conn.commit

conn.close