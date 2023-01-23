import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()


def get_cities_from_database() -> list[str]:
    connect = psycopg2.connect(dbname=os.environ.get('DATABASE_NAME'), user=os.environ.get('DATABASE_USER'),
                               password=os.environ.get('DATABASE_PASSWORD'), host=os.environ.get('DATABASE_HOST'))
    cursor = connect.cursor()
    cursor.execute('SELECT city_name FROM city')
    data = cursor.fetchall()
    cursor.close(), connect.close()
    data_list_from_db: list = [city[0].strip().lower().replace('ё', 'е').replace('-', ' ') for city in data]
    return data_list_from_db


cities = get_cities_from_database()
