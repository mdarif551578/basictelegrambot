from dotenv import load_dotenv
import telebot
import os
import google.generativeai as genai


load_dotenv()
TOKEN = os.getenv('TOKEN')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

bot = telebot.TeleBot(token=TOKEN)
genai.configure(api_key=GOOGLE_API_KEY)


@bot.message_handler(commands=["start"])
def start(message):
  bot.send_message(chat_id=message.chat.id, text=f"Hello {message.from_user.first_name} {message.from_user.last_name}!")


@bot.message_handler(commands=["help"])
def help(message):
  bot.send_message(
    chat_id=message.chat.id,
    text=f"""
    /start -> Welcome to the bot.
    /help -> Help instructions.
    /models -> To Get Available models.
    /gemini -> Ask something to the Google Gemini LLM.
    """
  )


def get_models() -> str:
  models = ""
  for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        models = models + m.name + "\n"
  return models

@bot.message_handler(commands=["models"])
def models(message):
  bot.send_message(chat_id=message.chat.id, text=get_models())


def get_response(prompt: str, model: str) -> str:
  model = genai.GenerativeModel('gemini-1.5-pro')
  response = model.generate_content(prompt)
  response.resolve()
  return response.text

@bot.message_handler(commands=["gemini"])
def gemini(message):
  prompt = message.text.replace("/gemini", "", count=1)
  prompt = prompt.split(" ")
  for i in range(0, len(prompt)):
    if prompt[0] == "":
      prompt.remove("")
    else:
      break
  if prompt[0].startswith("models/"):
    model = prompt[0].replace("models/", "")
  bot.send_message(
    chat_id=message.chat.id,
    text=get_response(prompt=prompt, model=model)
  )

# bot.infinity_polling(
#   timeout=60,
#   long_polling_timeout=60
# )


from flask import Flask

app = Flask(__name__)
@app.route("/")
def index():
    return "Hello, World!"

def run():
  app.run(port=8000, host="0.0.0.0", debug=True)

def runbot():
  bot.infinity_polling(
    timeout=60,
    long_polling_timeout=60
  )

import threading
thread_event = threading.Event()


thread_event.set()
thread = threading.Thread(target=runbot)
thread.start()

thread_event.set()
thread = threading.Thread(target=run)
thread.start()

