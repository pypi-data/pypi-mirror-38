import requests
import re
from lxml.html import fromstring
from .utils import date_from_pgn_date_header, year_from_pgn_date, pgn_similarity_ratio, new_session, parse_pgn
import logging
from django.utils.text import slugify
logger = logging.getLogger(__name__)


def get_game(game_id, session=None, markup=None):
    payload = {}
    if markup is None:
        if session is None:
            session = new_session()
        r = session.get(f'http://www.chessgames.com/perl/chessgame?gid={game_id}', timeout=30)
        r.raise_for_status()
        markup = r.text

    pgn_string = fromstring(markup).get_element_by_id('olga-data').get('pgn').strip()
    game = parse_pgn(pgn_string)
    headers = game.headers

    players = re.findall(r'\/perl\/chessplayer\?pid=(\d+)', markup)
    white_id = int(players[0])
    black_id = int(players[1])

    white_name = headers.get('White', '')
    black_name = headers.get('Black', '')

    payload['white_name'] = white_name
    payload['white_slug'] = slugify(white_name)
    payload['black_name'] = black_name
    payload['black_slug'] = slugify(black_name)

    tournament_match = re.search(r'\/perl\/chess\.pl\?tid=(\d+)\">(.*?)<\/a', markup)
    if tournament_match is not None:
        tournament_id, tournament_name = int(tournament_match.group(1)), tournament_match.group(2)
        payload['tournament_id'] = tournament_id
        payload['tournament_name'] = tournament_name

    payload['chessgames_pgn'] = pgn_string
    payload['year'] = year_from_pgn_date(headers.get('Date', ''))
    payload['date'] = date_from_pgn_date_header(headers.get('Date'))
    return payload


def update_video(video, session=None):
    game_id = video.chessgames_id

    if not game_id:
        white_name, black_name = video.extracted_players
        white_slug, black_slug = slugify(white_name), slugify(black_name)
        if video.white_name == "":
            video.white_name = white_name
        if video.white_slug == "":
            video.white_slug = slugify(white_name)
        if video.black_name == "":
            video.black_name = black_name
        if video.black_slug == "":
            video.black_slug = black_slug

        video.save()
        return

    payload = get_game(game_id, session=session)

    video.date_played = payload.pop('date')
    video.white_name = payload.pop('white_name')
    video.white_slug = payload.pop('white_slug')
    video.black_name = payload.pop('black_name')
    video.black_slug = payload.pop('black_slug')
    video.tournament_id = payload.pop('tournament_id', None)
    video.tournament_name = payload.pop('tournament_name', '')
    video.year = payload.pop('year', None)
    video.data.update(payload)
    video.save()


def get_best_match(video, session=None):

    if video.extracted_pgn is None:
        return None

    if session is None:
        session = new_session()
    r = session.get(video.chessgames_similar_game_search_url, timeout=30)
    r.raise_for_status()
    markup = r.text

    id_list = re.findall(r'\/perl\/chessgame\?gid=(\d+)', markup)

    logger.info(f'Found {len(id_list)} possible matches for video {video.id}')

    result_id = None

    if len(id_list) > 10:
        video.ignore = True
        video.error = f'Too many possible matches found: {len(id_list)}'
        video.save()
        return None

    for game_id in id_list:

        game_pgn = get_game_pgn(game_id, session=session)

        if pgn_similarity_ratio(game_pgn, video.extracted_pgn) > 0.8:
            result_id = game_id

    video.data['chessgames_success'] = bool(result_id)
    video.data['chessgames_id_list'] = id_list
    if result_id:
        video.chessgames_id = result_id

    video.save()

    return result_id


def get_game_pgn(game_id, session=None):
    if session is None:
        session = requests.Session()

    r = session.get(f'http://www.chessgames.com/perl/chessgame?gid={game_id}')
    r.raise_for_status()
    markup = r.text
    pgn = fromstring(markup).get_element_by_id('olga-data').get('pgn').strip()
    return pgn
