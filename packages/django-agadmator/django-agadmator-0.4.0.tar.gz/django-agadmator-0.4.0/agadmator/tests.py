import pathlib

from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from . import chessgames
from .utils import parse_pgn
from .models import Message
from .views import ContactView

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

class TestMessage(TestCase):

    def test_form_submission_creates_message(self):

        url = reverse('agadmator:contact')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # submit the form
        response = self.client.post(url, data={
            "name": "Test",
            "email": "test@example.com",
            "content": "Testing..."
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(("/", 302), response.redirect_chain)
        self.assertIn(ContactView.success_message.encode(), response.content)
        m = Message.objects.first()
        self.assertIsNotNone(m)
        self.assertEqual(m.name, "Test")
        self.assertEqual(m.email, "test@example.com")
        self.assertEqual(m.content, "Testing...")

