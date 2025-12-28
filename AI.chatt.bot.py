import base64
import mimetypes
from telebot import TeleBot
from google import genai
from google.genai import types

TOKEN = "7991664762:AAGgr8mknKNk8-hAhTCpRqwLMiotYmvsRGo"
API_KEY = "AIzaSyCBiyiOQvZRnDmMejLolkioIUMwHYkpeDQ"

bot = TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет, я-умный бот который поможет тебе изучить язык программирования Python напиши команду /help чтобы ознакомиться поподробнее")

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id, f"/start-перезапустить бота\n"
                                      f"чтобы использоывать бота не нужны никакие команды можешь сразу говорить интересующие тебя вопросы я на них с удовольсвтием отвечу, а можешь даже сразу задачки кидать мы их с тобой разберем")

def generate(prompt):
    client = genai.Client(api_key=API_KEY)
    model = "gemini-2.0-flash"

    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(
                    text=f"Ты — преподаватель Python. Объясни это ученику простыми словами:\n\n{prompt}"
                ),
            ],
        ),
    ]

    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=types.GenerateContentConfig(response_modalities=["TEXT"]),
    )


    return response.candidates[0].content.parts[0].text


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    prompt = message.text
    bot.send_message(message.chat.id, "Думаю над ответом...")

    try:
        result = generate(prompt)
        bot.send_message(message.chat.id, result)
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка: {e}")


if __name__ == "__main__":
    print("Бот запущен!")
    bot.infinity_polling()
