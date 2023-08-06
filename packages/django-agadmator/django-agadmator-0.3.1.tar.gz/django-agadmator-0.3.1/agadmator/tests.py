import pathlib

from django.test import SimpleTestCase

from . import chessgames
from .utils import parse_pgn


class TestChessgamesDataExtraction(SimpleTestCase):

    def test_game(self):
        markup = pathlib.Path(__file__, '../tests/chessgames_game.html').resolve().read_text(errors='ignore')

        data = chessgames.get_game(game_id=123, markup=markup)

        self.assertEqual(data['year'], 1961)
        self.assertEqual(data['white_name'], 'Lev Polugaevsky')
        self.assertEqual(data['white_slug'], 'lev-polugaevsky')
        self.assertEqual(data['tournament_name'], 'USSR Championship 1961a (1961)')
        self.assertEqual(data['tournament_id'], 79537)

    def test_pgn_headers(self):
        pgn = """
[Event "Biel"]
[Site "0:52:33-0:22:33"]
[Date "2018.07.22"]
[EventDate "2018.07.21"]
[Round "1"]
[Result "1-0"]
[White "Magnus Carlsen"]
[Black "David Navara"]
[ECO "D30"]
[WhiteElo "?"]
[BlackElo "?"]
[PlyCount "127"]
        
1. e4 e5
"""

        game = parse_pgn(pgn)

        expected = {
            'Event': 'Biel',
            'Site': '0:52:33-0:22:33',
            'Date': '2018.07.22',
            'EventDate': '2018.07.21',
            'Round': '1',
            'Result': '1-0',
            'White': 'Magnus Carlsen',
            'Black': 'David Navara',
            'ECO': 'D30',
            'WhiteElo': '?',
            'BlackElo': '?',
            'PlyCount': '127',
        }

        for key, val in game.headers.items():
            print(key, val)

        for key, val in expected.items():
            self.assertEqual(game.headers.get(key), val)
