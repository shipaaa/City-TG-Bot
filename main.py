"""
                      ______   ______          ______    ____  ________  __           ____    ____   ______
                     /_  __/  / ____/         / ____/   /  _/ /_  __/\ \/ /          / __ )  / __ \ /_  __/
                      / /    / / __          / /        / /    / /    \  /          / __  | / / / /  / /
                     / /    / /_/ /         / /___    _/ /    / /     / /          / /_/ / / /_/ /  / /
                    /_/     \____/          \____/   /___/   /_/     /_/          /_____/  \____/  /_/
"""
import logging
import os
import random

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, filters
from aiogram.utils import executor
from dotenv import load_dotenv

from lexicon import lexicon_ru
from services.services import (check_last_char, cities, create_bot_city,
                               find_new_char)

load_dotenv()

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

bot_token = os.environ.get('BOT_TOKEN')
dp = Dispatcher(Bot(token=bot_token))


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    """Приветствие, вывод кнопок"""
    buttons = ['Правила игры \U0001F4D6', 'Закончить игру 🔚', 'Начать игру \U0001F3AE']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*buttons)
    await message.answer(lexicon_ru.GREETINGS, reply_markup=keyboard)


@dp.message_handler(filters.Text(equals='Правила игры \U0001F4D6'))
async def rules_button(message: types.Message):
    """Правила игры при нажатии на кнопку"""
    await message.answer(lexicon_ru.RULES, parse_mode=types.ParseMode.HTML)


@dp.message_handler(filters.Text(equals='Закончить игру 🔚'))
async def end_game_button(message: types.Message):
    """Очистка городов при нажатии на кнопку"""
    if end_game_condition(message.chat.id) is True:
        await message.answer('Игра закончилась. Нажимай на кнопку 😉')
    else:
        await message.answer('Игра ещё не запущена. Нажми на кнопку 😇')


def end_game_condition(chat_id: int) -> bool:
    """Условие при котором игра считается завершенной"""
    global global_list
    new_global_list = []
    if len(global_list) != 0:
        for i in global_list:
            if i[0] != chat_id:
                new_global_list.append(i)
        global_list = new_global_list
        return True
    else:
        return False


def get_private_list_by_id(chat_id: int) -> list:
    """Заполняем специальный приватный список только теми городами пользователя и бота, чьи chat id одинаковые. Все это
    делается ради многопоточности, чтобы много людей смогли играть одновременно без каких либо ошибок"""
    return [i[1] for i in global_list if i[0] == chat_id]


def refresh_bot(chat_id: int) -> list:
    """Функция перезапуска если бот проиграл или если хотим начать заново"""
    global global_list
    new_global_list = []
    for i in global_list:
        if i[0] != chat_id:
            new_global_list.append(i)
        global_list = new_global_list
    return global_list


@dp.message_handler(filters.Text(equals=['Начать игру \U0001F3AE']))
async def game_start(message: types.Message):
    refresh_bot(message.chat.id)
    rnd_bt_ct = random.choice(cities)
    global_list.append([message.chat.id, rnd_bt_ct])
    await message.answer(
        f'Я называю город <b>"{rnd_bt_ct.title()}"</b>\nТебе на <b>"{find_new_char(rnd_bt_ct).capitalize()}"</b>',
        parse_mode=types.ParseMode.HTML)

    @dp.message_handler()
    async def game_continue(msg: types.Message):
        user_city = msg.text.strip().lower().replace('ё', 'е').replace('-', ' ')
        print(f'{msg.from_user.username} / {msg.text}')

        if user_city in cities:
            private_cities = get_private_list_by_id(msg.chat.id)
            if check_last_char(user_city, private_cities) is True:
                if user_city not in private_cities:
                    global_list.append([msg.chat.id, user_city])
                    random_bot_cities_list = create_bot_city(user_city, private_cities)
                    if len(random_bot_cities_list) != 0:
                        bot_city = random.choice(random_bot_cities_list)
                        global_list.append([msg.chat.id, bot_city])
                        await msg.answer(bot_city.title())
                        list_for_print = [i for i in global_list if i[0] == msg.chat.id]
                        print(f'Username: {msg.from_user.username} ⚡ / '
                              f'Chat ID: {msg.chat.id} / Cities: {list_for_print}')
                    else:
                        await msg.answer("Я не знаю больше городов на эту букву. Ты выиграл 😱")  # Вызываем Reset
                        refresh_bot(chat_id=msg.chat.id)
                else:
                    await msg.answer('Этот город уже был. Попробуй ещё раз 😌')
            else:
                await msg.answer(f'Город должен начинаться на <b>"{check_last_char(user_city, private_cities)}"</b>',
                                 parse_mode=types.ParseMode.HTML)  # Город не на ту букву
        else:
            await msg.answer('Некорректный город, введите ещё раз 😕')  # Такого города нет в .json файле


if __name__ == '__main__':
    global_list: list = []
    """Список всех пользователей и их городов (В начале игры у определенного пользователя пуст)"""

    executor.start_polling(dp, skip_updates=True)
