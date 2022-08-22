import telebot
from telebot import types
import os
from dotenv import load_dotenv
import logging

from schedule_data_parser import json_schedule_data


# set logger settings
logging.basicConfig(
                    filename='schedule_bot.log',
                    level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s',
                    )

# set dotenv settings
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def welcome(message: str) -> None:
    """Start bot commands and buttons"""
    # keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Когда у меня экзамены?")
    item2 = types.KeyboardButton("Какая у меня группа?")
    markup.add(item1, item2)

    bot.send_message(
        message.chat.id,
        "Привет! {0.first_name}!\nЯ - <b>{1.first_name}</b> бот, который"
        "подскажет тебе расписание.".format(
            message.from_user, bot.get_me()
        ),
        parse_mode="html",
        reply_markup=markup,
    )


@bot.message_handler(content_types=["text"])
def bot_message(message: str) -> None:
    """
    This function sends parsed schedule data
    to user when he makes a related request.
    """
    if message.chat.type == "private":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        # parsed_data
        sch_dct = json_schedule_data()[0]
        group = json_schedule_data()[1]

        # functions with encapsulated logic
        def week_day_picker(week_day: str) -> None:
            """
            Function handle given weekday, search it in json
            and send related data to the user
            """
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton(list(sch_dct.get(week_day).keys())[0])
            if week_day != 'Вс':
                item2 = types.KeyboardButton(list(sch_dct.get(week_day).keys())[1])
            back = types.KeyboardButton("Назад")
            markup.add(item1, item2, back)
            bot.send_message(
                message.chat.id,
                "Выбери число",
                reply_markup=markup
                )

        def date_picker(week_day: str, date: str) -> None:
            """
            Function handle given weekday and date,
            search date in json and send related data to the user
            """
            bot.send_message(
                message.chat.id,
                sch_dct.get(week_day)[date],
                reply_markup=markup
            )

        if message.text == "Какая у меня группа?":
            bot.send_message(message.chat.id, group)
        elif message.text == "Когда у меня экзамены?":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Пн")
            item2 = types.KeyboardButton("Вт")
            item3 = types.KeyboardButton("Ср")
            item4 = types.KeyboardButton("Чт")
            item5 = types.KeyboardButton("Пт")
            item6 = types.KeyboardButton("Сб")
            item7 = types.KeyboardButton("Вс")
            back = types.KeyboardButton("Назад")
            markup.add(item1, item2, item3, item4, item5, item6, item7, back)

            bot.send_message(
                message.chat.id,
                "Выбери день недели",
                reply_markup=markup
                )

        # if user picked weekday from Monday to Saturday
        elif message.text in ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]:
            global current_week_day
            current_week_day = message.text
            try:
                week_day_picker(current_week_day)
            except Exception as e:
                bot.send_message(message.chat.id, f"Ошибка запроса")
                logging.warning(e)

        # if user picked date from 13 to 25 June
        elif message.text in ["13 июня", "14 июня", "20 июня", "15 июня",
                            "16 июня", "17 июня", "18 июня", "19 июня",
                            "20 июня", "21 июня", "22 июня", "23 июня",
                            "24 июня", "25 июня"]:
            try:
                date_picker(current_week_day, message.text)
            except Exception as e:
                bot.send_message(message.chat.id, f"Ошибка запроса")
                logging.warning(e)

        # back button
        elif message.text == "Назад":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Когда у меня экзамены?")
            item2 = types.KeyboardButton("Какая у меня группа?")
            markup.add(item1, item2)

            bot.send_message(message.chat.id, "Назад", reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "Я не могу на это ответить")


# run bot
if __name__ == '__main__':
    bot.polling(none_stop=True)
