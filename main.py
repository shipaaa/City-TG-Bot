"""
                      ______   ______          ______    ____  ________  __           ____    ____   ______
                     /_  __/  / ____/         / ____/   /  _/ /_  __/\ \/ /          / __ )  / __ \ /_  __/
                      / /    / / __          / /        / /    / /    \  /          / __  | / / / /  / /
                     / /    / /_/ /         / /___    _/ /    / /     / /          / /_/ / / /_/ /  / /
                    /_/     \____/          \____/   /___/   /_/     /_/          /_____/  \____/  /_/
"""
import os
import logging
import json
import random
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, filters
from aiogram.utils import executor

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

bot_token = os.getenv("BOT_TOKEN")
dp = Dispatcher(Bot(token=bot_token))


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    """Приветствие, вывод кнопок"""
    buttons = ['Правила игры \U0001F4D6', 'Закончить игру 🔚', 'Начать игру \U0001F3AE']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*buttons)
    await message.answer(f'Привет, я бот для игры в города ✌🏻\nНажимай на кнопку и скорее начинай со мной играть 🤖',
                         reply_markup=keyboard)


@dp.message_handler(filters.Text(equals='Правила игры \U0001F4D6'))
async def rules_btn(message: types.Message):
    """Правила игры при нажатии на кнопку"""
    a = 'Игра начинается с любого названия города 🏙'
    b = 'Каждый из участников игры по очереди называет реальный город, название которого начинается на букву, ' \
        'которой заканчивается предыдущее название города (Например: Краков-Варшава-Афины)'
    c = 'Запрещается повторение городов.'
    d = 'Если город заканчивается на <i>"Ь", "Ъ", "Ы", "Й"</i>, то берется последняя возможная буква (Например: ' \
        'Грозный-Ногинск, Керчь-Чернобыль). ' \
        '<b>Город Йошкар-Ола не используется в игре</b>'
    e = 'В игре задействованы все существующие города России на данный момент '
    g = 'Хорошей игры 🍀'
    await message.answer(f'❕{a}\n❕{b}\n❕{d}\n❕{c}\n❕{e}🇷🇺\n❕{g}',
                         parse_mode=types.ParseMode.HTML)


@dp.message_handler(filters.Text(equals='Закончить игру 🔚'))
async def end_game(message: types.Message):
    """Очистка городов"""
    global global_list
    chat_id = message.chat.id
    new_global_list = []
    if len(global_list) != 0:
        for i in global_list:
            if i[0] != chat_id:
                new_global_list.append(i)
        global_list = new_global_list
        await message.answer('Игра закончилась. Нажимай на кнопку 😉')
    else:
        await message.answer('Игра ещё не запущена. Нажми на кнопку 😇')


def get_private_list_by_id(chat_id: int) -> list:
    # Заполняем специальный приватный список только теми городами пользователя и бота, чьи chat id одинаковые. Все это
    # делается ради многопоточности, чтобы много людей смогли играть одновременно без каких либо ошибок
    private_list = []
    for i in global_list:
        if i[0] == chat_id:
            private_list.append(i[1])
    return private_list


def find_new_char(word: str) -> str:
    """Подбор последней буквы"""
    for char in word[::-1]:
        if char in ['ь', 'ъ', 'ы', 'й']:
            continue
        else:
            break
    return char


def check_last_char(new_city: str, prev_cities: list):
    """Проверка на последнюю букву и вывод ошибки если это нужно"""
    if len(prev_cities) != 0:
        prev_city = prev_cities[-1]
        prev_city, new_city = prev_city.lower(), new_city.lower()
        if new_city[0] != find_new_char(prev_city):
            return find_new_char(prev_city).capitalize()
        else:
            return 'ok'
    else:
        return 'ok'


def create_bot_city(city: str, private_cities: list) -> list:
    """Подбор города для бота"""
    random_bot_city_list = []
    char = find_new_char(city)
    for city in cities:
        if city not in private_cities:
            if city.startswith(char):
                random_bot_city_list.append(city)
    return random_bot_city_list


def refresh(chat_id: int) -> list:
    """Функция перезапуска если бот проиграл"""
    global global_list
    new_global_list = []
    for i in global_list:
        if i[0] != chat_id:
            new_global_list.append(i)
        global_list = new_global_list
    return global_list


@dp.message_handler(filters.Text(equals=['Начать игру \U0001F3AE']))
async def game_start(message: types.Message):
    refresh(message.chat.id)
    rnd_bt_ct = random.choice(cities)
    global_list.append([message.chat.id, rnd_bt_ct])
    await message.answer(
        f'Я называю город <b>"{rnd_bt_ct.title()}"</b>\nТебе на <b>"{find_new_char(rnd_bt_ct).capitalize()}"</b>',
        parse_mode=types.ParseMode.HTML)

    @dp.message_handler()
    async def game_continue(message: types.Message):
        user_city = message.text.strip().lower().replace('ё', 'е').replace('-', ' ')
        print(f'{message.from_user.username} / {message.text}')

        if user_city in cities:
            private_cities = get_private_list_by_id(message.chat.id)
            if check_last_char(user_city, private_cities) == 'ok':
                if user_city not in private_cities:
                    global_list.append([message.chat.id, user_city])
                    b = create_bot_city(user_city, private_cities)
                    if len(b) != 0:
                        bot_city = random.choice(b)
                        global_list.append([message.chat.id, bot_city])
                        await message.answer(bot_city.title())
                        list_for_print = [i for i in global_list if i[0] == message.chat.id]
                        print(f'Username: {message.from_user.username} ⚡ / '
                              f'Chat ID: {message.chat.id} / Cities: {list_for_print}')
                    else:
                        await message.answer("Я не знаю больше городов на эту букву. Ты выиграл 😱")  # Вызываем Reset
                        refresh(chat_id=message.chat.id)
                else:
                    await message.answer('Этот город уже был. Попробуй ещё раз 😌')
            else:
                await message.answer(f'Город должен начинаться на <b>"{check_last_char(user_city, private_cities)}"</b>'
                                     , parse_mode=types.ParseMode.HTML)  # Город не на ту букву
        else:
            await message.answer('Некорректный город, введите ещё раз 😕')  # Такого города нет в .json файле


if __name__ == '__main__':
    json_obj = open('all_cities.json', 'r', encoding='utf-8')
    cities = [city['Город'].strip().lower().replace('ё', 'е').replace('-', ' ') for city in json.load(json_obj)]
    global_list = []  # Список всех пользователей и их городов (В начале игры у определенного пользователя пуст)

    executor.start_polling(dp, skip_updates=True)
