import requests
import lxml.html
import telebot
from telebot import types

#Parser
def lxml_page(html_text):
    tree = lxml.html.document_fromstring(html_text)
    text_original = tree.xpath("/html//text()")
    converted_list = []

    #removing unnecessary values in list
    for element in text_original:
        converted_list.append(element.strip())
    while '' in converted_list:
        converted_list.remove('')
    
    #removing "\n" in list
    symbols_removed = []
    for i in converted_list:
        symbols_removed.append(i.replace("\n", ""))

    #removing spaces in list
    global parsed
    parsed = []
    for y in symbols_removed:
        parsed.append(y.replace("   ", ""))
    return parsed

def main():
    url = "https://urfu.ru/api/schedule/groups/lessons/985237/20211017/"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    html_text = requests.get(url, headers=headers).text
    lxml_page(html_text)

if __name__ == "__main__":
    main()

#Bot
token = "1923420310:AAE3mwgJkGNAB2qL03HWY13cBuPQMUbgG2w"
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
            bot.send_message(message.chat.id, 'Группа Фт-570101')
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
            bot.send_message(message.chat.id, parsed[102] + " " + parsed[103] + " " + parsed[104] + " " + parsed[105] + " " + parsed[106] + " " + parsed[107] + "\n" + "\n" + parsed[108] + " " + parsed[109] + " " + parsed[110] + " " + parsed[111] + " " + parsed[112], reply_markup=markup)
        elif message.text == 'Вт':
            bot.send_message(message.chat.id, (parsed[114] + " " + parsed[115] + " " + parsed[116] + " " + parsed[117] + " " + parsed[118] + " " + parsed[119] + "\n" + "\n" + parsed[120] + " " + parsed[121] + " " + parsed[122] + " " + parsed[123] + " " + parsed[124]) + "\n" + "\n" + parsed[125] + " " + parsed[126] + " " + parsed[127] + " " + parsed[128] + " " + parsed[129], reply_markup=markup)
        elif message.text == 'Ср':
            bot.send_message(message.chat.id, (parsed[131] + " " + parsed[132] + " " + parsed[133] + " " + parsed[134] + " " + parsed[135] + " " + parsed[136] + "\n" + "\n" + parsed[137] + " " + parsed[138] + " " + parsed[139] + " " + parsed[140]) + " " + parsed[141] + "\n" + "\n" + parsed[142] + " " + parsed[143] + " " + parsed[144] + " " + parsed[145] + " " + parsed[146] + "\n" + "\n" + parsed[147] + " " + parsed[148] + " " + parsed[149] + " " + parsed[150] + " " + parsed[151], reply_markup=markup)
        elif message.text == 'Чт':
            bot.send_message(message.chat.id, (parsed[153] + " " + parsed[154] + " " + parsed[155] + " " + parsed[156] + " " + parsed[157] + " " + parsed[158] + "\n" + "\n" + parsed[159] + " " + parsed[160] + " " + parsed[161] + " " + parsed[162] + " " + parsed[163]) + "\n" + "\n" + parsed[164] + " " + parsed[165] + " " + parsed[166] + " " + parsed[167] + " " + parsed[168], reply_markup=markup)
        elif message.text == 'Пт':
            bot.send_message(message.chat.id, (parsed[170] + " " + parsed[171] + " " + parsed[172] + " " + parsed[173] + " " + parsed[174] + " " + parsed[175] + "\n" + "\n" + parsed[176] + " " + parsed[177] + " " + parsed[178] + " " + parsed[179] + " " + parsed[180]) + "\n" + "\n" + parsed[181] + " " + parsed[182] + " " + parsed[183] + " " + parsed[184] + " " + parsed[185], reply_markup=markup)
        elif message.text == 'Сб':
            bot.send_message(message.chat.id, 'Пар нет, отдыхай', reply_markup=markup)
        elif message.text == 'Вс':
            bot.send_message(message.chat.id, 'Пар нет, но завтра будут!', reply_markup=markup)
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