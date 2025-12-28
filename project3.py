import threading
import json
from time import sleep
from telebot import*

TOKEN = "7751691912:AAGJJP2UqykstcWFnSo_3NuUjWLKHYE3__o"
bot = TeleBot(TOKEN)
user_data={}

def save_data():
    with open("user_data.json", "w") as f:
        json.dump(user_data, f)

def load_data():
    global user_data
    try:
        with open("user_data.json", "r") as f:
            user_data = json.load(f)
    except FileNotFoundError:
        user_data = {}

load_data()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет, я-умный бот напоминающий пользователям пить воды, напиши команду /help чтобы ознакомиться поподробнее")

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id, f"/start-перезапустить бота\n"
                                      f"/setreminder-установить время напоминаний\n"
                                      f"/drunk-дать отчет по количеству выпитой воды\n"
                                      f"/status-количество выпитой воды и сколько еще осталось выпить\n"
                                      f"/settarget-установить цель выпитой воды на каждый день (мл)")
    bot.send_message(message.chat.id,f"напишите (/setreminder 3) чтобы настроить время напоминаний")

@bot.message_handler(commands=['settarget'])
def set_target(message):
    target = message.text.split()
    if len(target)>1 and target[1].isdigit():
        amount=int(target[1])
        bot.send_message(message.chat.id, f"Хорошо, ты должен выпить {amount} мл воды каждый день")
        if message.chat.id not in user_data:
            user_data[message.chat.id] = {}
        user_data[message.chat.id]['target'] = amount
        save_data()
    else:
        bot.send_message(message.chat.id, f"Неправильная команда попробуйте еще раз./help")

@bot.message_handler(commands=['setreminder'])
def set_reminder(message):
    reminder=message.text.split()
    if len(reminder) > 1:
        amount=float(reminder[1])
        bot.send_message(message.chat.id, f"Хорошо, поставил напоминание на каждые {amount} час(а)")
        threading.Thread(target=reminder_loop, args=(message.chat.id,amount), daemon=True).start()
    else:
        bot.send_message(message.chat.id, f"Неправильная команда попробуйте еще раз./help")

@bot.message_handler(commands=['drunk'])
def drunk(message):
    drink=message.text.split()
    if len(drink) > 1 and drink[1].isdigit():
        amount = int(drink[1])
        if message.chat.id in user_data:
            user_data[message.chat.id]['drunk'] = user_data[message.chat.id].get('drunk', 0) + amount
        else:
            user_data[message.chat.id] = {'drunk': amount}
        save_data()
        bot.send_message(message.chat.id, f"Молодец! Ты выпил {amount} мл воды. Проверь статус командой /status")
    else:
        bot.send_message(message.chat.id, "Неправильная команда, попробуйте ещё раз. /help")

@bot.message_handler(commands=['status'])
def status(message):
    if message.chat.id in user_data:
        data = user_data[message.chat.id]
        drink = data.get('drunk', 0)
        target = data.get('target', 2000)
        bot.send_message(message.chat.id, f"Воды выпито-{drink}/{target}мл\n")
        if drink<target:
            bot.send_message(message.chat.id, f"осталось выпить-{target-drink}мл")
        else:
            bot.send_message(message.chat.id, f"Ты на сегодня выпил рекомендованное количество воды! Поздравляю!!")
    else:
        bot.send_message(message.chat.id, "Данные не найдены. Сначала задай цель командой /settarget")

def reminder_loop(chat_id, amount):
    while True:
        sleep(amount * 3600)
        bot.send_message(chat_id, f"Прошло {amount} часа, пришла пора выпить воду!!! не забудь дать отчет по команде /drunk!!!")

#print("Бот запущен!")
bot.infinity_polling()
