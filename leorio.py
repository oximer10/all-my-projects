from telebot import*
import requests
TOKEN = "8409461343:AAEaZBw-HrcN6rKF3dMPaUrqZrNr5DHIAcY"
API_TOKEN="45b501a5dc9e6b27fa9d922b"
bot = TeleBot(TOKEN)
user_data={}
messages = {
    "ru": {
        "start": "Привет! Это бот для конвертаций валют, здесь ты можешь одним сообщением конвертировать любое количество денег с одной валюты на другую. Пропиши команду /help чтобы понять как работать с этим ботом",
        "help": 'Для конвертаций валют нужно написать как (кол-во денег, изначальная валюта, валюта в которую хочешь конвертировать). Например "100 USD KZT" или пропиши команду /button чтобы сделать это быстрее и не писать вручную.\nИспользуйте /lang ru или /lang en',
        "choose_base": "Выберите валюту:",
        "choose_target": "В какую из валют вы хотите конвертировать?",
        "choose_amount": "Выберите количество денег (или напишите сумму сами):",
        "wrong": "Ошибка: попробуйте снова"
    },
    "en": {
        "start": "Hello! This is a currency converter bot. You can convert any amount of money from one currency to another in one message. Type /help to see how to use this bot",
        "help": "To convert currencies, type (amount, base currency, target currency). Example: 100 USD KZT. Or use /button to make it easier.\nUse /lang ru or /lang en",
        "choose_base": "Choose the base currency:",
        "choose_target": "Choose the target currency:",
        "choose_amount": "Enter or choose the amount:",
        "wrong": "Error: please try again"
    }
}

def get_exchange_rate(base_currency,target_currency):
    url = f"https://v6.exchangerate-api.com/v6/{API_TOKEN}/latest/{base_currency}"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        rates=data['conversion_rates']
        return rates.get(target_currency)

@bot.message_handler(commands=["lang"])
def set_lang(message):
    lang = message.text.split()
    if len(lang) > 1 and lang[1] in ["ru", "en"]:
        user_data[message.chat.id] = {"lang": lang[1]}
        bot.send_message(message.chat.id, f"Язык изменен на {lang[1]}")
    else:
        bot.send_message(message.chat.id, "Используйте /lang ru или /lang en")

def get_lang(chat_id):
    return user_data.get(chat_id, {}).get("lang", "ru")

@bot.message_handler(commands=["start"])
def start(message):
    lang = get_lang(message.chat.id)
    bot.send_message(message.chat.id, messages[lang]["start"])

@bot.message_handler(commands=["help"])
def help(message):
    lang = get_lang(message.chat.id)
    bot.send_message(message.chat.id, messages[lang]["help"])

@bot.message_handler(commands=["button"])
def button(message):
    lang = get_lang(message.chat.id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    item1 = types.KeyboardButton("USD")
    item2 = types.KeyboardButton("KZT")
    item3 = types.KeyboardButton("EUR")
    item4 = types.KeyboardButton("JPY")
    item5 = types.KeyboardButton("RUB")
    item6 = types.KeyboardButton("CNY")
    item7 = types.KeyboardButton("GBP")
    item8 = types.KeyboardButton("AUD")
    markup.add(item1,item2,item3,item4,item5,item6,item7,item8)
    bot.send_message(message.chat.id, messages[lang]["choose_base"], reply_markup=markup)
    bot.register_next_step_handler(message, fast_convert1)

def fast_convert1(message):
    base=message.text
    lang = get_lang(message.chat.id)
    if base not in ["USD","KZT","EUR","JPY","RUB","CNY","GBP","AUD"]:
        bot.send_message(message.chat.id, messages[lang]["wrong"])
        return
    user_data[message.chat.id] = {"base_currency": base}
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    for cur in ["USD","KZT","EUR","JPY","RUB","CNY","GBP","AUD"]:
        if cur != base:
            markup.add(types.KeyboardButton(cur))
    bot.reply_to(message, messages[lang]["choose_target"], reply_markup=markup)
    bot.register_next_step_handler(message, fast_convert2)

def fast_convert2(message):
    target=message.text
    lang = get_lang(message.chat.id)
    if target not in ["USD","KZT","EUR","JPY","RUB","CNY","GBP","AUD"]:
        bot.send_message(message.chat.id, messages[lang]["wrong"])
        return
    user_data[message.chat.id]["target_currency"] = target
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
    item1 = types.KeyboardButton("1")
    item2 = types.KeyboardButton("10")
    item3 = types.KeyboardButton("100")
    item4 = types.KeyboardButton("500")
    item5 = types.KeyboardButton("1000")
    item6 = types.KeyboardButton("10000")
    markup.add(item1,item2,item3,item4,item5,item6)
    lang=get_lang(message.chat.id)
    bot.send_message(message.chat.id, messages[lang]["choose_amount"], reply_markup=markup)
    bot.register_next_step_handler(message, fast_convert3)


def fast_convert3(message):
    try:
        amount=float(message.text)
        data = user_data.get(message.chat.id)
        if not data or "base_currency" not in data or "target_currency" not in data:
            bot.send_message(message.chat.id, "Ошибка: начните заново /button")
            return
        base_currency = data['base_currency']
        target_currency = data['target_currency']
        exchange_rate = get_exchange_rate(base_currency.upper(), target_currency.upper())
        if exchange_rate:
            converted_amount = amount * exchange_rate
            converted_amount2 = exchange_rate
            lang = get_lang(message.chat.id)
            bot.reply_to(message, f"1 {base_currency.upper()}=={converted_amount2:.2f} {target_currency.upper()}\n"
                                       f"{amount} {base_currency.upper()}=={converted_amount:.2f} {target_currency.upper()}")

        else:
            bot.reply_to(message, 'Ошибка,неккоректная валюта или API')
    except ValueError:
        bot.reply_to(message, 'Ошибка, проверьте правильность ввода')

    user_data.pop(message.chat.id, None)

@bot.message_handler(content_types=["text"])
def convert_currency(message):
    try:
        amount,base_currency,target_currency =message.text.split()
        amount = (float(amount))
        exchange_rate = get_exchange_rate(base_currency.upper(),target_currency.upper())
        if exchange_rate:
            converted_amount = amount * exchange_rate
            bot.reply_to(message,f"{amount} {base_currency.upper()}=={converted_amount} {target_currency.upper()}")
        else:
            bot.reply_to(message,'Ошибка,неккоректная валюта или API')
    except ValueError:
        bot.reply_to(message, 'Ошибка, проверьте правильность ввода')



#print("Бот запущен!")
bot.infinity_polling()
