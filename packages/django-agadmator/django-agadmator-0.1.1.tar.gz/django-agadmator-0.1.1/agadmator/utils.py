import re
from datetime import datetime
from difflib import SequenceMatcher
from chess.pgn import read_game, StringExporter
from io import StringIO
from requests import Session


def parse_duration(s):
    s = s.strip()

    days, hours, mins, secs, ms = [None] * 5
    m = re.match(
        r'(?:(?:(?:(?P<days>[0-9]+):)?(?P<hours>[0-9]+):)?(?P<mins>[0-9]+):)?(?P<secs>[0-9]+)(?P<ms>\.[0-9]+)?Z?$', s)
    if m:
        days, hours, mins, secs, ms = m.groups()
    else:
        m = re.match(
            r'''(?ix)(?:P?
                (?:
                    [0-9]+\s*y(?:ears?)?\s*
                )?
                (?:
                    [0-9]+\s*m(?:onths?)?\s*
                )?
                (?:
                    [0-9]+\s*w(?:eeks?)?\s*
                )?
                (?:
                    (?P<days>[0-9]+)\s*d(?:ays?)?\s*
                )?
                T)?
                (?:
                    (?P<hours>[0-9]+)\s*h(?:ours?)?\s*
                )?
                (?:
                    (?P<mins>[0-9]+)\s*m(?:in(?:ute)?s?)?\s*
                )?
                (?:
                    (?P<secs>[0-9]+)(?P<ms>\.[0-9]+)?\s*s(?:ec(?:ond)?s?)?\s*
                )?Z?$''', s)
        if m:
            days, hours, mins, secs, ms = m.groups()
        else:
            m = re.match(r'(?i)(?:(?P<hours>[0-9.]+)\s*(?:hours?)|(?P<mins>[0-9.]+)\s*(?:mins?\.?|minutes?)\s*)Z?$', s)
            if m:
                hours, mins = m.groups()
            else:
                return None

    duration = 0
    if secs:
        duration += float(secs)
    if mins:
        duration += float(mins) * 60
    if hours:
        duration += float(hours) * 60 * 60
    if days:
        duration += float(days) * 24 * 60 * 60
    if ms:
        duration += float(ms)
    return duration


def clean_pgn(s):
    s = s.replace('[WhiteElo "?"]\n', '')
    s = s.replace('[BlackElo "?"]\n', '')
    s = s.replace('[Round "?"]\n', '')
    s = s.replace('[EventDate "?"]\n', '')
    return s.strip()


def extract_pgn(text):
    pgn = ''
    m = re.search(r'\n1\.\s?[a-zA-Z]+\d(.*)\n', text, re.MULTILINE)
    if m is not None:
        pgn = m.group(0)

    return pgn.strip()


def date_from_pgn_date_header(date_string):

    try:
        return datetime.strptime(date_string, '%Y.%m.%d').date()
    except ValueError:
        pass

    return None


def parse_pgn(pgn_string):
    return read_game(StringIO(pgn_string))


def normalize_pgn(pgn_string):
    game = parse_pgn(pgn_string)
    exporter = StringExporter(
        columns=None, headers=False, comments=False, variations=False
    )
    return game.accept(exporter).rstrip('* ')


def similarity_ratio(a, b):
    return SequenceMatcher(None, a, b).ratio()


def pgn_similarity_ratio(a, b):
    return similarity_ratio(normalize_pgn(a), normalize_pgn(b))


def year_from_pgn_date(date_string):
    # date_string could look like 1999.??.??
    match = re.search(r'([\d]{4})', date_string)
    return None if match is None else int(match.group(0))


def extract_players(text):
    # first try simple case where A vs B on new line

    m = re.search(r'^([\w \-_()]+)\s?vs\.?\s?([\w \-_()]+)$', text, re.MULTILINE | re.IGNORECASE)
    if m is not None:
        left = m.group(1).strip(' .')
        right = m.group(2).strip(' .')
        return left, right

    m = re.search(r'(\b[A-Z][\w\-]+\s?)+\b\s+(vs|Vs|VS)\.?\s+(\b[A-Z][\w\-]+\s?)+\b', text, re.MULTILINE)
    if m is None:
        return "", ""
    full = m.group(0)
    full = full.split('\n')[0]
    split_string = ''
    splitters = [
        ' vs ',
        ' Vs ',
        ' VS ',
        ' vs. ',
    ]
    for s in splitters:
        if s in full:
            split_string = s
    if not split_string:
        return '', ''
    left, right = full.split(split_string)
    left = left.strip(' .')
    right = right.strip(' .')
    return left, right


def new_session():
    session = Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0'
    })
    return session
