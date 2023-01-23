from models.models import get_cities_from_database


def create_bot_city(city: str, private_cities: list) -> list:
    """Подбор города для бота"""
    random_bot_cities_list = []
    char = find_new_char(city)
    for city in cities:
        if city not in private_cities:
            if city.startswith(char):
                random_bot_cities_list.append(city)
    return random_bot_cities_list


def find_new_char(word: str) -> str:
    """Подбор последней буквы"""
    for char in word[::-1]:
        if char in ['ь', 'ъ', 'ы', 'й']:
            continue
        else:
            break
    else:
        raise RuntimeError
    return char


def check_last_char(new_city: str, prev_cities: list) -> str | bool:
    """Проверка на последнюю букву и вывод ошибки если это нужно"""
    if len(prev_cities) != 0:
        prev_city = prev_cities[-1]
        prev_city, new_city = prev_city.lower(), new_city.lower()
        if new_city[0] != find_new_char(prev_city):
            return find_new_char(prev_city).capitalize()
        else:
            return True
    else:
        return True


cities = get_cities_from_database()
