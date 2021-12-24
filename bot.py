import telebot
from telebot import types

token = ""
bot = telebot.TeleBot(token)
 
@bot.message_handler(commands=['start'])
def welcome(message):
    sti = open('logo.png', 'rb')
    bot.send_sticker(message.chat.id, sti)
 
    #keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Когда у меня пары?")
    item2 = types.KeyboardButton("Какая у меня группа?")
 
    markup.add(item1, item2)
 
    bot.send_message(message.chat.id, "Привет! {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот, который подскажет тебе расписание.".format(message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup)
 
@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.chat.type == 'private':
        markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
        if message.text == 'Какая у меня группа?':
            bot.send_message(message.chat.id, 'None')
        elif message.text == 'Когда у меня пары?':
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            item4 = types.KeyboardButton("Пн")
            item5 = types.KeyboardButton("Вт")
            item6 = types.KeyboardButton("Ср")
            item7 = types.KeyboardButton("Чт")
            item8 = types.KeyboardButton("Пт")
            item9 = types.KeyboardButton("Сб")
            item10 = types.KeyboardButton("Вс")
            back = types.KeyboardButton("Назад")
            markup.add(item4, item5, item6, item7, item8, item9, item10, back)

            bot.send_message(message.chat.id, 'Выбери день недели', reply_markup=markup)

        elif message.text == 'Пн':
            bot.send_message(message.chat.id, '1', reply_markup=markup)
        elif message.text == 'Вт':
            bot.send_message(message.chat.id, '2', reply_markup=markup)
        elif message.text == 'Ср':
            bot.send_message(message.chat.id, '3', reply_markup=markup)
        elif message.text == 'Чт':
            bot.send_message(message.chat.id, '4', reply_markup=markup)
        elif message.text == 'Пт':
            bot.send_message(message.chat.id, '5', reply_markup=markup)
        elif message.text == 'Сб':
            bot.send_message(message.chat.id, '6', reply_markup=markup)
        elif message.text == 'Вс':
            bot.send_message(message.chat.id, '7', reply_markup=markup)
        elif message.text == 'Назад':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Когда у меня пары?")
            item2 = types.KeyboardButton("Какая у меня группа?")
            markup.add(item1, item2)
            
            bot.send_message(message.chat.id, 'Назад', reply_markup=markup)

        else:
            bot.send_message(message.chat.id, 'Я не могу на это ответить(')


#run bot
bot.polling(none_stop=True)
