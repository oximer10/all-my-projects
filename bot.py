from telebot import*
import requests
from re import*
TOKEN = "8123700052:AAH0MCMvHxAUfqp_v0NuD7KvCz8nnpsOnzY"
weather_TOKEN="209b7c5cc9ee459197d71700252009"
bot = TeleBot(TOKEN)

def get_weather(city):
    try:
        url = f"http://api.weatherapi.com/v1/current.json?key={weather_TOKEN}&q={city}&aqi=no"
        response = requests.get(url)
        data = response.json()

        if "error" not in data:
            data = response.json()
            city_name = data['location'] ['name']
            temp = data['current'] ['temp_c']
            condition = data['current']['condition'] ['text']
            humidity = data['current'] ['humidity']
            wind_speed = data['current']['wind_kph']
            weather_report=(
                    f"Погода в {city_name}:\n"
                    f"Температура: {temp}°С\n"
                    f"Состояние: {condition}\n"
                    f"Влажность:{humidity}% \n"
                    f"Ветер: {wind_speed} км/ч")
        else:
            weather_report="Не удалось получить данные о погоде. Проверьте правильность названия города."
    except requests.exceptions.RequestException:
        weather_report="Не удалось получить данные о погоде. Проверьте правильность названия города."
    return weather_report

def get_weather_forecast(city,days=3):
    try:
        url = f"http://api.weatherapi.com/v1/forecast.json?key={weather_TOKEN}&q={city}&days={days}&aqi=no"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            city_name = data['location']['name']
            forecast_days = data['forecast']['forecastday']
            forecast_report = [f"Прогноз погоды в {city_name} на {days} дней:\n"]

            for day in forecast_days:

                date = day['date']
                condition = day['day']['condition']['text']
                temp = day['day']['avgtemp_c']
                humidity = day['day']['avghumidity']
                wind_speed = day['day']['maxwind_kph']
                forecast_report.append(
                    f" {date}:\n"
                    f"Cостояние:{condition}\n"
                    f"Средняя температура {temp}°C\n"
                    f"Влажность:{humidity}%\n"
                    f"Скорость ветра:{wind_speed}км/ч"
                )
            return "\n".join(forecast_report)
        else:
            weather_report = "Не удалось получить данные о погоде. Проверьте правильность названия города."
    except requests.exceptions.RequestException:
        weather_report = "Не удалось получить данные о погоде. Проверьте правильность названия города."
    return weather_report


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id,"Доступные команды:\n"
                                     "/start — запустить бота\n"
                                     "/help — помощь\n"
                                     "/button — показать кнопки\n")

@bot.message_handler(commands=["help"])
def help1(message):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    item1 = types.KeyboardButton('Сейчас')
    markup.add(item1)
    item2 = types.KeyboardButton('Прогноз')
    markup.add(item2)
    bot.send_message(message.chat.id,"Привет! Я-Telegram-бот который описывает погоду в любом городе, напишите мне название города на английском, и я скажу вам погоду в этом городе!")
    bot.send_message(message.chat.id,'Введи "Сейчас" чтобы узнать погоду в текущее время или введите "Прогноз" чтобы узнать погоду на следующие дни', reply_markup=markup)


@bot.message_handler(content_types=["text"])
def vibor(message):
    if message.text == "Прогноз":
        bot.send_message(message.chat.id, "Введите название города(на английском) и то на какой день сделать прогноз:")
        bot.register_next_step_handler(message, send_weather_forecast)
    elif message.text == "Сейчас":
        bot.send_message(message.chat.id, "Введите название города (на английском):")
        bot.register_next_step_handler(message, send_weather)
    else:
        bot.send_message(message.chat.id, 'Неверная команда. Используйте кнопки или команды /help.')

@bot.message_handler(commands=["button"])
def button_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Moscow")
    markup.add(item1)
    item2 = types.KeyboardButton("Almaty")
    markup.add(item2)
    item3 = types.KeyboardButton("Astana")
    markup.add(item3)
    item4 = types.KeyboardButton("Shymkent")
    markup.add(item4)
    item5 = types.KeyboardButton("New-York")
    markup.add(item5)
    bot.send_message(message.chat.id, 'Кнопки активировались', reply_markup=markup)

def send_weather(message):
    city = message.text
    weather_report = get_weather(city)
    bot.send_message(message.chat.id,weather_report)

def send_weather_forecast(message):
    numbers = findall(r'\d+', message.text)
    days = int(numbers[0]) if numbers else 3
    city = sub(r'\d+', '', message.text).strip()
    forecast = get_weather_forecast(city, days)
    bot.send_message(message.chat.id, forecast)





#print("Бот запущен!")
bot.infinity_polling()
