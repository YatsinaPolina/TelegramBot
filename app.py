from flask import Flask, request
import requests
from dotenv import load_dotenv
import os
from os.path import join, dirname
from lxml import html

app = Flask(__name__)


def get_joke():
    joke_content = []
    page = requests.get('https://anekdot-z.ru/random-anekdot').content
    html_tree = html.fromstring(page)
    items = html_tree.xpath('//p/span/text()')
    for item in items:
        joke_content.append(item)
    return joke_content


def joke_text(joke_content):
    joke = '\n'.join(joke_content)
    return joke


def get_from_env(key):
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)
    return os.environ.get(key)


def send_message(chat_id, text):
    method = "sendMessage"
    token = get_from_env("TELEGRAM_BOT_TOKEN")
    url = f"https://api.telegram.org/bot{token}/{method}"
    data = {"chat_id": chat_id, "text": text}
    requests.post(url, data=data)


@app.route('/', methods=["POST"])
def process():
    chat_id = request.json["message"]["chat"]["id"]
    send_message(chat_id=chat_id, text=joke_text(get_joke()))
    return {"ok": True}


if __name__ == '__main__':
    app.run()
