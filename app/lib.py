import re


class InvalidMove(Exception):
    pass


class ParseMoveError(Exception):
    pass


def parse_player_move(req):
    s = str(req['request']['original_utterance'])
    match = re.match(r'(\D+)([0-9]+)(\D+)([0-9]+)', s, re.I)
    if match:
        items = match.groups()
        result = ''
        try:
            result += str(parse_char(items[0]))
            result += str(parse_num(items[1]))
            result += str(parse_char(items[2]))
            result += str(parse_num(items[3]))

        except ValueError:
            raise ParseMoveError()

        return result
    else:
        raise ParseMoveError()


def parse_num(s):
    n = int(s)
    if 1 <= n <= 8:
        return n
    else:
        raise ValueError()


converter = [
    ('h', ['аш', 'эйч', 'ш', 'эш']),
    ('g', ['жи', 'ж', 'джи', 'жы']),
    ('f', ['ф', ]),
    ('e', ['е', 'йэ', 'и']),
    ('d', ['д']),
    ('c', ['ц']),
    ('b', ['б', 'в']),
    ('a', ['а']),
]


def parse_char(s):
    s = s.lower()
    for simple in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']:
        if simple in s:
            return simple

    for char, arr in converter:
        for elem in arr:
            if elem in s:
                return char

    raise ValueError()
