from django.test import TestCase, SimpleTestCase
import pathlib
# from .models import Player, Tournament, Game
from .utils import clean_pgn, extract_pgn, date_from_pgn_date_header, parse_pgn
from . import chessgames


class TestDataExtraction(TestCase):

    def test_game(self):
        g = Game(id=123)
        html = pathlib.Path(__file__, '../tests/game.html').resolve().read_text()
        g.update(markup=html)
        self.assertEqual(g.white_id, 12295)
        self.assertEqual(g.black_id, 50065)
        self.assertEqual(g.tournament_id, 93549)
        self.assertEqual(g.eco, 'A14')
        self.assertEqual(g.pgn, """[Event "Grand Chess Tour Paris (Rapid)"]
[Site "Paris FRA"]
[Date "2018.06.20"]
[EventDate "2018.06.20"]
[Round "3"]
[Result "1-0"]
[White "Vladimir Kramnik"]
[Black "Shakhriyar Mamedyarov"]
[ECO "A14"]
[WhiteElo "2792"]
[BlackElo "2808"]
[PlyCount "98"]

1. Nf3 Nf6 2. g3 d5 3. Bg2 e6 4. O-O Be7 5. c4 O-O 6. b3 c5 7. cxd5 Nxd5 8. Bb2 Nc6 9. d4 cxd4 10. Nxd4 Nxd4 11. Qxd4 Bf6 12. Qd2 Nf4 13. gxf4 Qxd2 14. Nxd2 Bxb2 15. Rab1 Bf6 16. Rbc1 Rd8 17. Ne4 Be7 18. Rc7 Kf8 19. Rfc1 Rb8 20. e3 h6 21. Bf3 a5 22. Kg2 g5 23. fxg5 hxg5 24. h3 f5 25. Nc5 b6 26. Na4 Bd6 27. Rh7 Kg8 28. Ra7 Be5 29. Rc6 Rd6 30. Rxd6 Bxd6 31. Nc3 b5 32. Rxa5 b4 33. Nb5 Bc5 34. Nd4 Bxd4 35. exd4 Kf7 36. Ra7+ Kf6 37. Rc7 Ba6 38. d5 Bb7 39. d6 Bxf3+ 40. Kxf3 Rd8 41. Rb7 Rxd6 42. Rxb4 e5 43. a4 e4+ 44. Ke2 Ke5 45. a5 f4 46. Ra4 f3+ 47. Ke1 Rc6 48. a6 Rc1+ 49. Kd2 Rf1 1-0""")

    def test_tournament(self):
        html = pathlib.Path(__file__, '../tests/tournament.html').resolve().read_text(errors='ignore')
        t = Tournament(id=123)
        t.update(markup=html)
        self.assertEqual(t.name, 'Grand Chess Tour Paris (Rapid) Tournament')

    def test_player(self):
        html = pathlib.Path(__file__, '../tests/player.html').resolve().read_text(errors='ignore')
        p = Player(id=123)
        p.update(markup=html)
        self.assertEqual(p.name, 'Vladimir Kramnik')


class TestUtils(SimpleTestCase):

    def test_clean_pgn(self):
        s = """
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

1.d4 Nf6 2.Nf3 d5 3.c4 e6 4.Bg5 Bb4+ 5.Nc3 h6 6.Bxf6 Qxf6 7.e3 O-O 8.Rc1 dxc4 9.Bxc4 c5 10.dxc5 Nd7 11.O-O Nxc5 12.Nb5 a6 13.Nbd4 b5 14.Be2 e5 15.Nc2 Rd8 16.Nxb4 Rxd1 17.Rfxd1 a5 18.Nd5 Qd6 19.Nxe5 Bb7 20.Bf3 Rc8 21.Ng4 Qf8 22.h4 Nd7 23.Rxc8 Bxc8 24.a3 h5 25.Nh2 g6 26.Be2 Ne5 27.Bxb5 Bb7 28.Nc3 Qe7 29.Rd4 Qe6 30.Nf1 Qb3 31.Rd2 Nc4 32.Rd7 Nxb2 33.Rxb7 Qxc3 34.Be8 Kf8 35.Bxf7 Qc6 36.Rxb2 Kxf7 37.Rd2 Qa4 38.Rd3 Qxh4 39.Rd7+ Kg8 40.Rd4 Qe7 41.a4 Qa3 42.g3 Qa1 43.Kg2 g5 44.Nd2 g4 45.Ne4 Qc1 46.Nf6+ Kf7 47.Nxh5 Qc6+ 48.Kg1 Qc1+ 49.Kh2 Kg6 50.Nf4+ Kf6 51.Ng2 Kg5 52.Rf4 Qd1 53.Nh4 Qc2 54.Nf5 Qd3 55.e4 Qd7 56.e5 Qh7+ 57.Kg1 Qg6 58.Nd6 Qe6 59.Rf5+ Qxf5 60.Nxf5 Kxf5 61.f4 gxf3 62.Kf2 Kxe5 63.Kxf3 Kf5 64.Ke3 1-0
        """

        expected = """[Event "Biel"]
[Site "0:52:33-0:22:33"]
[Date "2018.07.22"]
[EventDate "2018.07.21"]
[Round "1"]
[Result "1-0"]
[White "Magnus Carlsen"]
[Black "David Navara"]
[ECO "D30"]
[PlyCount "127"]

1.d4 Nf6 2.Nf3 d5 3.c4 e6 4.Bg5 Bb4+ 5.Nc3 h6 6.Bxf6 Qxf6 7.e3 O-O 8.Rc1 dxc4 9.Bxc4 c5 10.dxc5 Nd7 11.O-O Nxc5 12.Nb5 a6 13.Nbd4 b5 14.Be2 e5 15.Nc2 Rd8 16.Nxb4 Rxd1 17.Rfxd1 a5 18.Nd5 Qd6 19.Nxe5 Bb7 20.Bf3 Rc8 21.Ng4 Qf8 22.h4 Nd7 23.Rxc8 Bxc8 24.a3 h5 25.Nh2 g6 26.Be2 Ne5 27.Bxb5 Bb7 28.Nc3 Qe7 29.Rd4 Qe6 30.Nf1 Qb3 31.Rd2 Nc4 32.Rd7 Nxb2 33.Rxb7 Qxc3 34.Be8 Kf8 35.Bxf7 Qc6 36.Rxb2 Kxf7 37.Rd2 Qa4 38.Rd3 Qxh4 39.Rd7+ Kg8 40.Rd4 Qe7 41.a4 Qa3 42.g3 Qa1 43.Kg2 g5 44.Nd2 g4 45.Ne4 Qc1 46.Nf6+ Kf7 47.Nxh5 Qc6+ 48.Kg1 Qc1+ 49.Kh2 Kg6 50.Nf4+ Kf6 51.Ng2 Kg5 52.Rf4 Qd1 53.Nh4 Qc2 54.Nf5 Qd3 55.e4 Qd7 56.e5 Qh7+ 57.Kg1 Qg6 58.Nd6 Qe6 59.Rf5+ Qxf5 60.Nxf5 Kxf5 61.f4 gxf3 62.Kf2 Kxe5 63.Kxf3 Kf5 64.Ke3 1-0"""

        self.assertEqual(clean_pgn(s), expected)

    def test_extract_pgn(self):
        text = """Robert James Fischer vs Borislav Ivkov
Palma de Mallorca Interzonal (1970), Palma de Mallorca ESP, rd 13, Nov-27
Spanish Game: Closed Variations. Smyslov Defense (C93)

1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 4. Ba4 Nf6 5. O-O Be7 6. Re1 b5 7. Bb3 d6 8. c3 O-O 9. h3 h6 10. d4 Re8 11. Be3 Bf8 12. Nbd2 Bb7 13. Qb1 Qb8 14. a3 Nd8 15. Bc2 c6 16. b4 Qc7 17. Bd3 Ne6 18. Qc2 Rac8 19. a4 Nd7 20. Qb3 Nf4 21. Bf4 ef4 22. c4 bc4 23. Bc4 d5 24. Bd3 Rb8 25. Qc3 Qb6 26. Reb1 Ba8 27. a5 Qa7 28. e5 Rb7 29. Qc6 Bb4 30. Qa6 Qb8 31. Bc2 Re6 32. Qd3 Nf8 33. Qf5 Ra6 34. Nb3 g6 35. Qf4 Bc3 36. Nc5 Ra5 37. Nb7 Ra1 38. Ra1 Ne6 39. Qf6 Ba1 40. Nd6 Qc7 41. Bg6 Qc1 42. Ne1 Qe1 43. Kh2 Ng5 44. Bf7
---
If you realllly enjoy my content, you're welcome to support me and my channel with a small donation via PayPal, Bitcoin, Litecoin or Nano."""
        expected = """1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 4. Ba4 Nf6 5. O-O Be7 6. Re1 b5 7. Bb3 d6 8. c3 O-O 9. h3 h6 10. d4 Re8 11. Be3 Bf8 12. Nbd2 Bb7 13. Qb1 Qb8 14. a3 Nd8 15. Bc2 c6 16. b4 Qc7 17. Bd3 Ne6 18. Qc2 Rac8 19. a4 Nd7 20. Qb3 Nf4 21. Bf4 ef4 22. c4 bc4 23. Bc4 d5 24. Bd3 Rb8 25. Qc3 Qb6 26. Reb1 Ba8 27. a5 Qa7 28. e5 Rb7 29. Qc6 Bb4 30. Qa6 Qb8 31. Bc2 Re6 32. Qd3 Nf8 33. Qf5 Ra6 34. Nb3 g6 35. Qf4 Bc3 36. Nc5 Ra5 37. Nb7 Ra1 38. Ra1 Ne6 39. Qf6 Ba1 40. Nd6 Qc7 41. Bg6 Qc1 42. Ne1 Qe1 43. Kh2 Ng5 44. Bf7"""
        self.assertEqual(extract_pgn(text), expected)

    def test_date_from_pgn(self):
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

1.d4 Nf6 2.Nf3 d5 3.c4 e6 4.Bg5 Bb4+ 5.Nc3 h6 6.Bxf6 Qxf6 7.e3 O-O 8.Rc1 dxc4 9.Bxc4 c5 10.dxc5 Nd7 11.O-O Nxc5 12.Nb5 a6 13.Nbd4 b5 14.Be2 e5 15.Nc2 Rd8 16.Nxb4 Rxd1 17.Rfxd1 a5 18.Nd5 Qd6 19.Nxe5 Bb7 20.Bf3 Rc8 21.Ng4 Qf8 22.h4 Nd7 23.Rxc8 Bxc8 24.a3 h5 25.Nh2 g6 26.Be2 Ne5 27.Bxb5 Bb7 28.Nc3 Qe7 29.Rd4 Qe6 30.Nf1 Qb3 31.Rd2 Nc4 32.Rd7 Nxb2 33.Rxb7 Qxc3 34.Be8 Kf8 35.Bxf7 Qc6 36.Rxb2 Kxf7 37.Rd2 Qa4 38.Rd3 Qxh4 39.Rd7+ Kg8 40.Rd4 Qe7 41.a4 Qa3 42.g3 Qa1 43.Kg2 g5 44.Nd2 g4 45.Ne4 Qc1 46.Nf6+ Kf7 47.Nxh5 Qc6+ 48.Kg1 Qc1+ 49.Kh2 Kg6 50.Nf4+ Kf6 51.Ng2 Kg5 52.Rf4 Qd1 53.Nh4 Qc2 54.Nf5 Qd3 55.e4 Qd7 56.e5 Qh7+ 57.Kg1 Qg6 58.Nd6 Qe6 59.Rf5+ Qxf5 60.Nxf5 Kxf5 61.f4 gxf3 62.Kf2 Kxe5 63.Kxf3 Kf5 64.Ke3 1-0
        """

        expected = '2018-07-22'

        self.assertEqual(date_from_pgn(pgn).strftime('%Y-%m-%d'), expected)


class TestChessgamesDataExtraction(SimpleTestCase):

    def test_game(self):
        markup = pathlib.Path(__file__, '../tests/chessgames_game.html').resolve().read_text(errors='ignore')

        data = chessgames.get_game(game_id=123, markup=markup)

        white = {
            'chessgames_id': 13741,
            'name': 'Lev Polugaevsky'
        }

        tournament = {
            'chessgames_id': 79537,
            'name': 'USSR Championship 1961a (1961)'
        }

        self.assertEqual(data['year'], 1961)
        self.assertEqual(data['headers']['ECO'], 'C98')
        self.assertDictEqual(data['white'], white)
        self.assertDictEqual(data['tournament'], tournament)

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
        
        xxx
        """

        headers = parse_pgn(pgn).headers
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
        self.assertDictEqual(headers, expected)
