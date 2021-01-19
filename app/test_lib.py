from unittest import TestCase

from app.lib import parse_player_move, ParseMoveError


def test_adapter(s):
    return parse_player_move({'request': {'original_utterance': s}})


class Test(TestCase):

    def test_simple_moves(self):
        for elem in ['e2e4', 'a1a4', 'b2c6', 'd3g6', 'f8h3']:
            self.assertEqual(test_adapter(elem), elem)

    def test_bounds_moves(self):
        for elem in ['l2m4', 'a0b9']:
            with self.assertRaises(ParseMoveError):
                test_adapter(elem)

    def test_complex_moves(self):
        for in_, out_ in [('Аш 7 Аш 5', 'h7h5')]:
            self.assertEqual(test_adapter(in_), out_)


