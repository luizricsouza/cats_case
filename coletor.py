
import sqlite3
import requests
import json
import settings

db_file = settings.db_file
sql_create_breeds_table = settings.sql_create_breeds_table

url = settings.cats_api_url
url_images = settings.cats_images_url
headers = {
    'x-api-key': settings.cats_api_key
}

def get_cats():
    response = requests.get(url, headers=headers, verify=False)
    cats = json.loads(response.text)

    return cats

def get_cats_infos(raw_cats):
    cats_list = [(cat['id'], cat['name'], cat['temperament'], cat['origin'], cat['description']) for cat in raw_cats]

    return cats_list

def get_cats_images(cat_id):
    url = '{}?breed_id={}&limit=3'.format(url_images, cat_id)
    response = requests.get(url, headers=headers, verify=False)

    cat_images = json.loads(response.text)

    return cat_images

raw_cats = get_cats()
cats = get_cats_infos(raw_cats)

conn = sqlite3.connect(db_file)
cursor = conn.cursor()

cursor.execute(sql_create_breeds_table)

cursor.executemany('INSERT INTO breeds VALUES (?, ?, ?, ?, ?)', cats)

conn.commit()

conn.close()