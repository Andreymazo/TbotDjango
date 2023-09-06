from django.core.management import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User 
import telebot 
from telebot import types
from config import settings

get_user_model()
bot = telebot.TeleBot(settings.Token)

# @bot.message_handler(commands=['start', 'button'])
@bot.message_handler(commands=['start'])
def start(message):
    if message.text == '/start':
        
        markup = types.InlineKeyboardMarkup(row_width=1) 
        item1 = types.InlineKeyboardButton('Посмотреть пользовательское соглашение', callback_data='first')
        item2 = types.InlineKeyboardButton('Принять условия пользовательского соглашения', callback_data='second')
        item3 = types.InlineKeyboardButton('Отклонить условия пользовательского соглашения', callback_data='third')
        markup.add(item1, item2, item3)
        # url = 'https://'
        # markup.add(types.InlineKeyboardButton('Открыть пользовательское соглашение', url=url))
        bot.send_message(message.chat.id, '<b>Privet</b>', parse_mode='html', reply_markup=markup)
        # with open("polzov_soglash.txt", "rb") as f: 
        #   contents = f.read().decode("UTF-8") 
        #   bot.reply_to(message, contents)
    else:
        bot.send_message(message.chat.id, 'Я вас не понимаю, надо набрать /start')

@bot.message_handler(commands=['phonenumber'])
def phone(message):
        print('5555555555555555')
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button_phone = types.KeyboardButton(text="Отправить телефон",
                                            request_contact=True)
        keyboard.add(button_phone)
        bot.send_message(message.chat.id, 'Номер телефона',
                         reply_markup=keyboard)

@bot.message_handler(content_types=['contact'])
def contact(message):
    print('6666666666666666', message.contact.phone_number)
    if message.contact is not None:
        keyboard2 = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'Вы успешно отправили свой номер', reply_markup=keyboard2)
        global phonenumber
        phonenumber= str(message.contact.phone_number)
        user_id = str(message.contact.user_id)
        print('7777777777777777777777777777777777777', phonenumber, user_id)

@bot.callback_query_handler(func=lambda call:True)
def callback(call):
    if call.message:
        if call.data == 'first':
            # markup = types.InlineKeyboardMarkup(row_width=1) 
            # item2 = types.InlineKeyboardButton('Принять условия пользовательского соглашения', callback_data='second')
            # item3 = types.InlineKeyboardButton('Отклонить условия пользовательского соглашения', callback_data='third')
            # markup.add(item2, item3)
            with open("polzov_soglash.txt", "rb") as f: 
                contents = f.read().decode("UTF-8") 
            bot.send_message(call.message.chat.id, contents)
            

        elif call.data == 'second':
            # Proverka vvoda s telefonom i proch
            bot.send_message(call.message.chat.id, f'Введите ваш номер телефона')
            phone(call.message)
            contact(call.message)
            if call.message.text==phonenumber:
                  bot.send_message(call.message.chat.id, 'Порядок')
            else:
                bot.send_message(call.message.chat.id, f"Непорядок, ваш номер {phonenumber}")
                # j = User.objects.create(username=f'{call.message.from_user.id}')
                # j.save()
        elif call.data == 'third':
            bot.send_message(call.message.chat.id, 'Так не пойдет')
            # with open("polzov_soglash.txt", "rb") as f: 
            #     contents = f.read().decode("UTF-8") 
            #     bot.reply_to(message, contents)
            #     j = User.objects.create(username=f'{message.from_user.id}')
            #     j.save()
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
