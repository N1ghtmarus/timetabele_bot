import requests
import lxml.html
import telebot
from telebot import types
import os

from dotenv import load_dotenv


# Parser
def lxml_page(html_text):
    tree = lxml.html.document_fromstring(html_text)
    text_original = tree.xpath("/html//text()")

    # removing unnecessary values in list
    no_spaces_text = [i.strip() for i in text_original if i.strip() != ""]

    # removing "\n" in list
    prepared_text = [i.replace('\n', '').replace('   ', '') for i in
                     no_spaces_text]
    group = prepared_text[1]
    schedule = prepared_text[2::]

    # making schedule json
    shedule_dict = dict()
    current_slice = 0
    for _ in range(13):
        current = schedule[current_slice::]
        if "июня" in current[2]:
            if not shedule_dict.get(current[1]):
                shedule_dict[current[1]] = {}
            shedule_dict[current[1]][current[0]] = "Сегодня экзаменов нет"
            current_slice += 2

        else:
            shedule_join = " ".join(current[1:7:])
            if not shedule_dict.get(current[1]):
                shedule_dict[current[1]] = {}
            shedule_dict[current[1]][current[0]] = shedule_join
            current_slice += 7
    return shedule_dict, group


def main():
    url = "https://urfu.ru/api/schedule/groups/lessons/46278/20220613/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5)"
        "AppleWebKit/537.36 (KHTML, like Gecko)"
        "Chrome/50.0.2661.102 Safari/537.36"
    }
    html_text = requests.get(url, headers=headers).text
    return lxml_page(html_text)


# Bot
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def welcome(message):
    # sti = open('logo.png', 'rb')
    # bot.send_sticker(message.chat.id, sti)

    # keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Когда у меня экзамены?")
    item2 = types.KeyboardButton("Какая у меня группа?")

    markup.add(item1, item2)

    bot.send_message(
        message.chat.id,
        "Привет! {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот, который"
        "подскажет тебе расписание.".format(
            message.from_user, bot.get_me()
        ),
        parse_mode="html",
        reply_markup=markup,
    )


@bot.message_handler(content_types=["text"])
def bot_message(message):
    if message.chat.type == "private":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        sch_dct = main()[0]
        group = main()[1]
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

        # Monday
        elif message.text == "Пн":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton(list(sch_dct.get("Пн").keys())[0])
            item2 = types.KeyboardButton(list(sch_dct.get("Пн").keys())[1])
            back = types.KeyboardButton("Назад")
            markup.add(item1, item2, back)
            bot.send_message(
                message.chat.id,
                "Выбери число",
                reply_markup=markup
                )

        elif message.text == "13 июня":
            bot.send_message(
                message.chat.id,
                sch_dct.get("Пн")["13 июня"],
                reply_markup=markup
            )

        elif message.text == "20 июня":
            bot.send_message(
                message.chat.id,
                sch_dct.get("Пн")["20 июня"],
                reply_markup=markup
            )

        # Tuesday
        elif message.text == "Вт":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton(list(sch_dct.get("Вт").keys())[0])
            item2 = types.KeyboardButton(list(sch_dct.get("Вт").keys())[1])
            back = types.KeyboardButton("Назад")
            markup.add(item1, item2, back)
            bot.send_message(
                message.chat.id,
                "Выбери число",
                reply_markup=markup
                )

        elif message.text == "14 июня":
            bot.send_message(
                message.chat.id,
                sch_dct.get("Вт")["14 июня"],
                reply_markup=markup
            )

        elif message.text == "21 июня":
            bot.send_message(
                message.chat.id,
                sch_dct.get("Вт")["21 июня"],
                reply_markup=markup
            )

        # Wednesday
        elif message.text == "Ср":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton(list(sch_dct.get("Ср").keys())[0])
            item2 = types.KeyboardButton(list(sch_dct.get("Ср").keys())[1])
            back = types.KeyboardButton("Назад")
            markup.add(item1, item2, back)
            bot.send_message(
                message.chat.id,
                "Выбери число",
                reply_markup=markup
                )

        elif message.text == "15 июня":
            bot.send_message(
                message.chat.id,
                sch_dct.get("Ср")["15 июня"],
                reply_markup=markup
            )

        elif message.text == "22 июня":
            bot.send_message(
                message.chat.id,
                sch_dct.get("Ср")["22 июня"],
                reply_markup=markup
            )

        # Thursday
        elif message.text == "Чт":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton(list(sch_dct.get("Чт").keys())[0])
            item2 = types.KeyboardButton(list(sch_dct.get("Чт").keys())[1])
            back = types.KeyboardButton("Назад")
            markup.add(item1, item2, back)
            bot.send_message(
                message.chat.id,
                "Выбери число",
                reply_markup=markup
                )

        elif message.text == "16 июня":
            bot.send_message(
                message.chat.id,
                sch_dct.get("Чт")["16 июня"],
                reply_markup=markup
            )

        elif message.text == "23 июня":
            bot.send_message(
                message.chat.id,
                sch_dct.get("Чт")["23 июня"],
                reply_markup=markup
            )

        elif message.text == "Назад":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Когда у меня экзамены?")
            item2 = types.KeyboardButton("Какая у меня группа?")
            markup.add(item1, item2)

            bot.send_message(message.chat.id, "Назад", reply_markup=markup)

        # Friday
        elif message.text == "Пт":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton(list(sch_dct.get("Пт").keys())[0])
            item2 = types.KeyboardButton(list(sch_dct.get("Пт").keys())[1])
            back = types.KeyboardButton("Назад")
            markup.add(item1, item2, back)
            bot.send_message(
                message.chat.id,
                "Выбери число",
                reply_markup=markup
                )

        elif message.text == "17 июня":
            bot.send_message(
                message.chat.id,
                sch_dct.get("Пт")["17 июня"],
                reply_markup=markup
            )

        elif message.text == "24 июня":
            bot.send_message(
                message.chat.id,
                sch_dct.get("Пт")["24 июня"],
                reply_markup=markup
            )

        # Saturday
        elif message.text == "Сб":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton(list(sch_dct.get("Сб").keys())[0])
            item2 = types.KeyboardButton(list(sch_dct.get("Сб").keys())[1])
            back = types.KeyboardButton("Назад")
            markup.add(item1, item2, back)
            bot.send_message(
                message.chat.id,
                "Выбери число",
                reply_markup=markup
                )

        elif message.text == "18 июня":
            bot.send_message(
                message.chat.id,
                sch_dct.get("Сб")["18 июня"],
                reply_markup=markup
            )

        elif message.text == "25 июня":
            bot.send_message(
                message.chat.id,
                sch_dct.get("Сб")["25 июня"],
                reply_markup=markup
            )

        # Sunday
        elif message.text == "Вс":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton(list(sch_dct.get("Вс").keys())[0])
            back = types.KeyboardButton("Назад")
            markup.add(item1, back)
            bot.send_message(
                message.chat.id,
                "Выбери число",
                reply_markup=markup
                )

        elif message.text == "19 июня":
            bot.send_message(
                message.chat.id,
                sch_dct.get("Вс")["19 июня"],
                reply_markup=markup
            )

        # back
        elif message.text == "Назад":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Когда у меня экзамены?")
            item2 = types.KeyboardButton("Какая у меня группа?")
            markup.add(item1, item2)

            bot.send_message(message.chat.id, "Назад", reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "Я не могу на это ответить(")


# run bot
bot.polling(none_stop=True)
