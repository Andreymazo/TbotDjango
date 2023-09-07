from django.core.management import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User 
import telebot 
from telebot import types
from config import settings

name = ''
surname = ''
tlf = 0
bot = telebot.TeleBot(settings.Token)
get_user_model()

@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/reg':
        markup = types.InlineKeyboardMarkup(row_width=1)#, resize_keyboard=True) 
        item = types.InlineKeyboardButton('Принять условия пользовательского соглашения', callback_data='accept')
        markup.add(item)
        with open("polzov_soglash.txt", "rb") as f: 
            contents = f.read().decode("UTF-8") 
            bot.send_message(message.chat.id, contents, reply_markup=markup)
    else:
        bot.send_message(message.from_user.id, 'Напиши /reg')

def get_name(message): #получаем фамилию
    global name
    name = message.text
    bot.send_message(message.from_user.id, 'Какая у тебя фамилия?')
    bot.register_next_step_handler(message, get_surname)
    print('name', name)

def get_surname(message):
    global surname
    surname = message.text
    bot.send_message(message.from_user.id, 'Номер вашего телефона?')
    bot.register_next_step_handler(message, get_tlf)

def get_tlf(message):
    global tlf
    # while tlf == 0: #проверяем что возраст изменился
    #     try:
    #          tlf = int(message.text) #проверяем, что  введен корректно
    #     except Exception:
    #          bot.send_message(message.from_user.id, 'Цифрами, пожалуйста')
    tlf = message.text
    keyboard = types.InlineKeyboardMarkup() #наша клавиатура
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
    key_no= types.InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.add(key_yes,key_no)
    question = 'Ваш телефон '+str(tlf)+' вас зовут '+name+' '+surname+'?'
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)

#  этот хендлер сработает только на тех, у которых callback_data начинается с bike_model
# @bot.callback_query_handler(func=lambda call: call.data.startswith('bike_model'))
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == 'accept':
        mes = bot.send_message(call.message.chat.id, "Как тебя зовут?")
        bot.register_next_step_handler(mes, get_name) 

    if call.data == "yes": 
       
        username_lst = User.objects.all().values_list('username', flat=True)
        print('username_lst', username_lst)
        print('name, surname', name, surname)
        if not str(name + surname + tlf) in username_lst:
            
            j = User.objects.all().create(username=str(name + surname + tlf))
            j.save() 
            bot.send_message(call.message.chat.id, 'Запомню : )')
        else:
            bot.send_message(call.message.chat.id, 'Уже есть у нас в базе : )')
            
    elif call.data == "no":
        bot.send_message(call.message.chat.id, 'Напиши /reg')

bot.polling(non_stop=True)

class Command(BaseCommand):

    def handle(self, *args, **options):
        
        from django.db import connection
        db_name = connection.settings_dict['NAME']
        print(db_name)