import json
import random


def city_json(json_file='all_cities.json'):
    global json_obj
    try:
        json_obj = open(json_file, 'r', encoding='utf-8')
        py_obj = json.load(json_obj)
    except Exception as err:
        print(err)
        return None
    finally:
        json_obj.close()
    return [city['Город'].strip().lower().replace('ё', 'е').replace('-', ' ') for city in
            py_obj]  # Список городов, которые знает бот


cities = city_json()
print(cities)

cities_already_said = set()


def main(input_city):
    user_city = input_city.strip().lower().replace('ё', 'е').replace('-', ' ')
    if user_city in cities:
        if main.prev_city != '' and user_city[0] != main.prev_city[-1] and user_city[0] != main.prev_city[-2]:  # !!!!!
            if main.prev_city[-1] in ['ь', 'ъ', 'ы']:
                print(f'Город должен начинаться на "{main.prev_city[-2].capitalize()}"')
            else:
                print(f'Город должен начинаться на "{main.prev_city[-1].capitalize()}"')
        else:
            if user_city not in cities_already_said:
                cities_already_said.add(user_city)
                last_latter_city = user_city[-1]
                proposed_names = list(filter(lambda x: x[0] == last_latter_city, cities))
                if proposed_names:
                    for city in proposed_names:
                        if city not in cities_already_said:
                            cities_already_said.add(city)
                            main.prev_city = city
                            print(city.capitalize())
                            return city.capitalize
                print('Я не знаю города на эту букву. Ты выиграл')
                bot_city_list = []
                if user_city[-1] in ['ь', 'ъ', 'ы']:
                    for i in cities:
                        if i.startswith(user_city[-2]):
                            bot_city_list.append(i)
                else:
                    for j in cities:
                        if j.startswith(user_city[-1]):
                            bot_city_list.append(j)
                main.prev_city = random.choice(bot_city_list)
                cities_already_said.add(main.prev_city)
                print(main.prev_city.capitalize())
                bot_city_list.clear()
                return main.prev_city.capitalize()

            else:
                print('Такой город уже был')
    else:
        print('Некорректное название города')


main.prev_city = ''

if __name__ == '__main__':
    print('Введите ваш город:')
    while True:
        main(input())
