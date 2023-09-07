from django.core.management import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User 
import telebot 
from telebot import types
from config import settings

get_user_model()
bot = telebot.TeleBot(settings.Token)

# @bot.message_handler(commands=['start', 'button'])
# @bot.message_handler(commands=['start'])
@bot.message_handler(content_types=['text'])
def start(message):
    if message.text.lower()  == 'start':
        
        markup = types.InlineKeyboardMarkup(row_width=1) 
        item1 = types.InlineKeyboardButton('Посмотреть пользовательское соглашение', callback_data='first')
        # item2 = types.InlineKeyboardButton('Принять условия пользовательского соглашения', callback_data='second')
        # item3 = types.InlineKeyboardButton('Отклонить условия пользовательского соглашения', callback_data='third')
        markup.add(item1)
        # url = 'https://'
        # markup.add(types.InlineKeyboardButton('Открыть пользовательское соглашение', url=url))
        bot.send_message(message.chat.id, '<b>Privet</b>', parse_mode='html', reply_markup=markup)#
    else:
        bot.send_message(message.chat.id, 'Я вас не понимаю, надо набрать start')
##################################
# bot.register_next_step_handler
# https://www.youtube.com/watch?v=yFdzGEAYiiE
###################################
# @bot.message_handler(commands=['phonenumber'])

######################################## Tak zanosit srazu i prosto potom vidergivat ################
# @bot.message_handler(content_types=['contact'])
# def phone_name(message):
#         print('5555555555555555')
#         keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
#         button_contact = types.KeyboardButton(text="Отправить данные",
#                                             request_contact=True)
        
#         keyboard.add(button_contact)
#         if message.contact:
#             print('here iiiiiiiiii')
#             bot.send_message(message.chat.id, message.contact.phone_number, reply_markup=keyboard)
######################################################################################################
@bot.message_handler(content_types=['text'])
def phone_name(message):
    # https://telegra.ph/Pishem-svoego-telegram-bota-na-Python-ch2-12-13
    # https://ru.stackoverflow.com/questions/705633/%D0%9A%D0%B0%D0%BA-%D0%BF%D0%BE%D0%BB%D1%83%D1%87%D0%B8%D1%82%D1%8C-%D1%81%D0%BE%D0%BE%D0%B1%D1%89%D0%B5%D0%BD%D0%B8%D0%B5-%D0%BE%D1%82-usera-%D0%BA%D0%BE%D1%82%D0%BE%D1%80%D0%BE%D0%B5-%D0%BE%D0%BD-%D0%BE%D1%82%D0%BF%D1%80%D0%B0%D0%B2%D0%B8%D0%BB-%D0%B2-%D0%BE%D1%82%D0%B2%D0%B5%D1%82-%D0%BD%D0%B0-%D1%81%D0%BE%D0%BE%D0%B1%D1%89%D0%B5%D0%BD%D0%B8%D0%B5-%D0%B1%D0%BE%D1%82%D0%B0?ysclid=lm8a86wq43972552168

    # mm = types.ReplyKeyboardMarkup(row_width=2)
    # keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    button_name = types.InlineKeyboardButton("😎 Введите имя", callback_data='name')
    button_phone = types.InlineKeyboardButton("😥 Введите телефон", callback_data='phone')
    # button_name = types.KeyboardButton(text="Отправить имя")
    # button_phone = types.KeyboardButton(text="Отправить телефон")
    # button1 = types.KeyboardButton("🐣 Привет")
    # button2 = types.KeyboardButton("😀 Как дела?")
    keyboard.add(button_name, button_phone)
    bot.send_message(message.chat.id, f'{message.text}', reply_markup=keyboard)


@bot.message_handler(commands=['command'])
def _command_(message):
     bot.send_message(message.chat.id, "Введите имя: ")
     bot.register_next_step_handler(message, add_user)

def add_user(message):
    #тут функция записи в бд
    j = User.objects.create(id = f'{message.from_user.id}', first_name=f'{message.text}')
    j.save()
    
# https://ru.stackoverflow.com/questions/1280092/%D0%9F%D0%BE%D0%BB%D1%83%D1%87%D0%B5%D0%BD%D0%B8%D0%B5-%D0%BD%D0%BE%D0%BC%D0%B5%D1%80%D0%B0-%D1%82%D0%B5%D0%BB%D0%B5%D1%84%D0%BE%D0%BD%D0%B0-%D0%BF%D0%BE%D1%81%D0%BB%D0%B5-%D0%BE%D1%82%D0%BF%D1%80%D0%B0%D0%B2%D0%BA%D0%B8-%D0%B5%D0%B3%D0%BE-%D0%B2-telegram?ysclid=lm7qppa83o668821030
# @bot.message_handler(content_types=['contact'])
# def contact(message):
#     print('6666666666666666', message.contact.phone_number)
#     if message.contact is not None:
#         keyboard2 = types.ReplyKeyboardRemove()
#         bot.send_message(message.chat.id, 'Вы успешно отправили свой номер', reply_markup=keyboard2)
#         global phonenumber
#         phonenumber= str(message.contact.phone_number)
#         user_id = str(message.contact.user_id)
#         print('7777777777777777777777777777777777777', phonenumber, user_id)

@bot.callback_query_handler(func=lambda call:True)
def callback(call):
    if call.message:
        if call.data == 'first':
            markup = types.InlineKeyboardMarkup(row_width=1)#, resize_keyboard=True) 
            item2 = types.InlineKeyboardButton('Принять условия пользовательского соглашения', callback_data='second')
            item3 = types.InlineKeyboardButton('Отклонить условия пользовательского соглашения', callback_data='third')
            markup.add(item2, item3)
           
            # markup = types.InlineKeyboardMarkup(row_width=1) 
            # item2 = types.InlineKeyboardButton('Принять условия пользовательского соглашения', callback_data='second')
            # item3 = types.InlineKeyboardButton('Отклонить условия пользовательского соглашения', callback_data='third')
            # markup.add(item2, item3)
            with open("polzov_soglash.txt", "rb") as f: 
                contents = f.read().decode("UTF-8") 
            bot.send_message(call.message.chat.id, contents, reply_markup=markup)
            

        elif call.data == 'second':
            # Proverka vvoda s telefonom i proch
            # bot.send_message(call.message.chat.id, f'Введите ваши данные')
            phone_name(call.message)
            # contact(call.message)
            # if call.message.text==phonenumber:
            #       bot.send_message(call.message.chat.id, 'Порядок')
            # else:
            #     bot.send_message(call.message.chat.id, f"Непорядок, ваш номер {phonenumber}")
                # j = User.objects.create(username=f'{call.message.from_user.id}')
                # j.save()
        elif call.data == 'third':
            bot.send_message(call.message.chat.id, 'Так не пойдет')
            # with open("polzov_soglash.txt", "rb") as f: 
            #     contents = f.read().decode("UTF-8") 
            #     bot.reply_to(message, contents)
            #     j = User.objects.create(username=f'{message.from_user.id}')
            #     j.save()
        elif call.data == 'name':
            print(f'name {call.message.text}')
        elif call.data == 'phone':
            print(f'phone {call.message.text}')

# @bot.message_handler(content_types=["text"])
# def answer(message):
#     if message.text == message.contact.phone_number:
#         bot.send_message(message.chat.id, 'Информация о вашей машине:...')
# @bot.message_handler(content_types=['text'])
# def handle_message(message):
#     bot.reply_to(message, message.text)

bot.polling(non_stop=True)

class Command(BaseCommand):

    def handle(self, *args, **options):
        
        from django.db import connection
        db_name = connection.settings_dict['NAME']
        print(db_name)
