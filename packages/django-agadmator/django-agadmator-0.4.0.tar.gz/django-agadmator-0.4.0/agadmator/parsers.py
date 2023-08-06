from urllib.parse import urlparse, parse_qs


def chessgames_player(html_element):
    root = html_element
    name = html_element.cssselect('p b')[0].text
    tables = html_element.cssselect('table')
    try:
        description = tables[10].cssselect('p')[0].text
    except IndexError:
        description = ''

    return {
        'name': name,
        'description': description
    }


def player_directory(html_element):
    anchors = html_element.cssselect('a')
    players = []
    for a in anchors:
        href = a.get('href')
        if not href.startswith('/perl/chessplayer'):
            continue
        try:
            pid = parse_qs(urlparse(href).query).get('pid')[0]
        except (IndexError, TypeError):
            continue

        players.append({
            'url': href,
            'name': a.text_content(),
            'id': pid
        })

    return {
        'players': players
    }
