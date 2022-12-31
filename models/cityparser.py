import time

import ujson
from bs4 import BeautifulSoup

stTime = time.time()
with open('index.html', encoding='utf-8') as file:
    src = file.read()


def main():
    soup = BeautifulSoup(src, 'lxml')
    table = soup.find('tbody').find_all('tr')
    all_cities_ld = []
    for item in table:
        city_element = item.find_all('td')[2:3]
        region_element = item.find_all('td')[3:4]
        date_element = item.find_all('td')[6:7]
        for city in city_element:
            if 'не призн.' in city.text:
                a = city.text.replace('не призн.', '')
                city_elements = a.replace('\n', '')
            else:
                city_elements = city.text.replace('\n', '')
        for region in region_element:
            region_elements = region.text.replace('\n', '')
        for date in date_element:
            d = date.find('a')
            date_elements = d.text.replace('\n', '')
            all_dict = {'Город': city_elements, 'Регион': region_elements, 'Дата основания': date_elements}
            all_cities_ld.append(all_dict)
    print(all_cities_ld)
    with open('all_cities.json', 'w', encoding='utf-8') as f:
        ujson.dump(all_cities_ld, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    main()
    endTime = time.time()
    print(f'Program was finished in {endTime - stTime} seconds...')
