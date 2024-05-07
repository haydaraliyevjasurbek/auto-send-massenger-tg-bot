import telebot
from telebot import types
import time

bot = telebot.TeleBot('7143835507:AAH8QhKA7OgzNxrmnEdmgccxHhEyzlqNVqI')

ADMIN_ID = 5489200661
stop = True
channel = ""
interval = 0
message_text = ""

@bot.message_handler(commands=['start'])
def start(message):
    if message.from_user.id == ADMIN_ID:
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton(text='🛠️Kanalni sozlash', callback_data='kanal')
        button2 = types.InlineKeyboardButton(text='🕓Oraliq(Interval)', callback_data='oraliq')
        button3 = types.InlineKeyboardButton(text="Xabarni taxrirlash", callback_data='xabar')
        button4 = types.InlineKeyboardButton(text='🚀Xabarni yuborish', callback_data="send")
        markup.add(button1)
        markup.add(button2)
        markup.add(button3)
        markup.add(button4)
        bot.send_message(message.chat.id, "O'zingizga kerakli bo'limni tanlang:", reply_markup=markup)
    else:
        bot.reply_to(message, "Siz admin emmasiz!")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'kanal':
        bot.send_message(call.message.chat.id, "Botni kanal/guruhga admin qilib quying❕❕❕\nKanalni(Guruhni) xuddi shunday tarzda kiriting: @kanal_username")
        bot.register_next_step_handler(call.message, save_channel)
    elif call.data == 'oraliq':
        bot.send_message(call.message.chat.id, "Oraliq ulchovi: daqiqa\nOraliqni sonlar orqali kiriting:")
        bot.register_next_step_handler(call.message, process_interval_step)
    elif call.data == 'xabar':
        bot.send_message(call.message.chat.id, "Xabar matnini kiriting:")
        bot.register_next_step_handler(call.message, process_message_step)
    elif call.data == 'send':
        bot.send_message(call.message.chat.id, "Agar xabarni hozir yubormoqchi bo'lsangiz, 1 raqamini yozib qoldiring\n\nAgar xabarni oraliq bo'yicha yubormoqchi bo'lsangiz, 2 raqamini yozib qoldiring:")
        bot.register_next_step_handler(call.message, process_message_send)

def save_channel(message):
    global channel
    channel = message.text
    bot.send_message(message.chat.id, "Kanal saqlandi✅")

def process_interval_step(message):
    global interval
    interval = int(message.text)
    bot.send_message(message.chat.id, "Oraliq saqlandi✅")

def process_message_step(message):
    global message_text
    message_text = message.text
    bot.send_message(message.chat.id, "Xabar saqlandi✅")

def process_message_send(message):
    global channel, interval, message_text, stop
    if message.text == '1':
        bot.reply_to(message, "Habar yuborildi✅")
        bot.send_message(channel, message_text)
    elif message.text == '2':
        bot.reply_to(message, "Habar oraliq buyicha yuborilish boshlandi✅\n/stop buyrug'ini bosing, agar oraliqni to'xtatmoqchi bo'lsangiz")
        while stop:
            bot.send_message(channel, message_text)
            time.sleep(interval * 60)

@bot.message_handler(commands=['stop'])
def stop_message(message):
    global stop
    stop = False
    bot.reply_to(message, "Oraliq to'xtatildi✅")

bot.infinity_polling()