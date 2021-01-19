# coding: utf-8
# Импортирует поддержку UTF-8.
from __future__ import unicode_literals

# Импортируем модули для работы с JSON и логами.
import json
import logging
from stockfish import Stockfish
import sys

from .lib import InvalidMove, ParseMoveError, parse_player_move

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
            'moves': []
        }

        res['response']['text'] = 'Ты играешь белыми, начинай'
        res['response']['buttons'] = [{'title': 'e2e4', 'hide': True}]
        return

    if str(req['request']['original_utterance']).lower().startswith("зано"):
        sessionStorage[user_id]['moves'] = []
        res['response']['text'] = "Чтоже, начнем новую партию"
        res['response']['buttons'] = [{'title': 'e2e4', 'hide': True}]

    elif 'отмени' in req['request']['nlu']['tokens']:
        rejected_moves = sessionStorage[user_id]['moves'][-2:]
        sessionStorage[user_id]['moves'] = sessionStorage[user_id]['moves'][:-2]
        stockfish.set_position(sessionStorage[user_id]['moves'])

        res['response']['text'] = "Отменяю свой ход " + rejected_moves[1] + ' и ваш ход ' + rejected_moves[0]
        res['response']['buttons'] = [{'title': stockfish.get_best_move_time(2000), 'hide': True}, {'title': 'Отмени', 'hide': True}, {'title': 'Заново', 'hide': True}]
    else:
        try:
            move = parse_player_move(req)
        except ParseMoveError as e:
            res['response']['text'] = "Не поняла какой ход вы имели ввиду, попробуйте еще раз"
            res['response']['buttons'] = [{'title': 'Отмени', 'hide': True}, {'title': 'Заново', 'hide': True}]
            return

        stockfish.set_position(sessionStorage[user_id]['moves'])
        if not stockfish.is_move_correct(move):
            res['response']['text'] = "К сожалению, этот ход нельзя сделать"
            res['response']['buttons'] = [{'title': stockfish.get_best_move_time(2000), 'hide': True}]
            return

        sessionStorage[user_id]['moves'].append(move)
        stockfish.set_position(sessionStorage[user_id]['moves'])
        alice_move = stockfish.get_best_move_time(2000)

        sessionStorage[user_id]['moves'].append(alice_move)
        stockfish.set_position(sessionStorage[user_id]['moves'])

        res['response']['text'] = alice_move # + " " + str(stockfish.get_evaluation())
        res['response']['buttons'] = [{'title': stockfish.get_best_move_time(2000), 'hide': True}, {'title': 'Отмени', 'hide': True}, {'title': 'Заново', 'hide': True}]


if __name__ == "__main__":
    app.run()
