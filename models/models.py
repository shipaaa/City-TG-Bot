import sqlite3


def get_cities_from_database() -> list[str]:
    con = sqlite3.connect("./models/db.sqlite3")
    cursor = con.cursor()
    cursor.execute("""SELECT city_name FROM city""")
    data = cursor.fetchall()
    data_list_from_db: list = [city[0].strip().lower().replace('ё', 'е').replace('-', ' ') for city in data]

    return data_list_from_db
