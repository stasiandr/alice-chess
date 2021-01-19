# coding: utf-8
# Импортирует поддержку UTF-8.
from __future__ import unicode_literals

# Импортируем модули для работы с JSON и логами.
import json
import logging
from stockfish import Stockfish
import sys

# Импортируем подмодули Flask для запуска веб-сервиса.
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


logging.basicConfig(level=logging.DEBUG)

# Хранилище данных о сессиях.
sessionStorage = {}

# Initializing engine

stockfish_parameters = {
    "Write Debug Log": "true",
    "Skill Level": 3,
    "Slow Mover": 10,
}

stockfish = Stockfish("/usr/local/bin/stockfish", parameters=stockfish_parameters)

# Задаем параметры приложения Flask.
@app.route("/", methods=['POST'])
def main():
# Функция получает тело запроса и возвращает ответ.
    logging.info('Request: %r', request.json)

    response = {
        "version": request.json['version'],
        "session": request.json['session'],
        "response": {
            "end_session": False
        }
    }

    handle_dialog(request.json, response)

    logging.info('Response: %r', response)

    return json.dumps(
        response,
        ensure_ascii=False,
        indent=2
    )

# Функция для непосредственной обработки диалога.
def handle_dialog(req, res):
    user_id = req['session']['user_id']

    if req['session']['new']:
        # Это новый пользователь.
        # Инициализируем сессию и поприветствуем его.

        sessionStorage[user_id] = {
            'moves' : []
        }

        res['response']['text'] = 'Ты играешь белыми, начинай'
        res['response']['buttons'] = [ {'title' : 'е2е4', 'hide' : True} ]
        return

    move = parse_player_move(req)
    sessionStorage[user_id]['moves'].append(move)
    stockfish.set_position(sessionStorage[user_id]['moves'])
    alice_move = stockfish.get_best_move()

    print(sessionStorage[user_id]['moves'], file=sys.stdout)

    sessionStorage[user_id]['moves'].append(alice_move)
    stockfish.set_position(sessionStorage[user_id]['moves'])


    print(sessionStorage[user_id]['moves'], file=sys.stdout)

    res['response']['text'] = alice_move
    res['response']['buttons'] = [ {'title' : stockfish.get_best_move(), 'hide' : True} ]


def parse_player_move(req):
    #parse will go here

    return req['request']['original_utterance']




if __name__ == "__main__":
    app.run()