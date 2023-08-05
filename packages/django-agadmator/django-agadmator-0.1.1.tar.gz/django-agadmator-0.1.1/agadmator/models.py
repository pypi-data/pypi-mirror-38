import logging
import re
from urllib.parse import urlencode

from django.contrib.postgres.fields import JSONField
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.db import models
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.text import slugify
from .utils import extract_pgn, extract_players
from chess.pgn import read_game, StringExporter
from io import StringIO
from .exporters import MarkupExporter, FenExporter

logger = logging.getLogger(__name__)


class Video(models.Model):
    youtube_id = models.CharField(blank=True, max_length=100, db_index=True)
    title = models.CharField(max_length=500, blank=True)
    time_updated = models.DateTimeField(auto_now=True)
    time_published = models.DateTimeField(blank=True, null=True, db_index=True)
    date_played = models.DateField(blank=True, null=True, db_index=True)
    description = models.TextField(blank=True)
    data = JSONField(default=dict, blank=True)
    chessgames_id = models.BigIntegerField(blank=True, null=True, db_index=True)
    search_vector = SearchVectorField(null=True)
    stream = models.BooleanField(default=False, db_index=True)  # if video is YT stream
    engine = models.BooleanField(default=False, db_index=True)   # if one of the players is engine
    ignore = models.BooleanField(default=False, db_index=True)  # if video is not fit for normal parsing
    error = models.TextField(blank=True)
    """
    data keys:
       
        white: {
            name: str
            slug: str
            chessgames_id: str
        }
        black: {
            name: str
            slug: str
            chessgames_id: str
        }
        chessgames_id_list: [str]  // used for auto game matching
        chessgames_success: bool    // if auto matching succeeded
        chessgames_pgn: str
        tournament: {
            name: str
            chessgames_id: str
        }                   // name of tournament this game is part of
        duration: int       // video duration in seconds (from youtube_dl)
        tags: [str]         // tags from youtube
        
    """

    def __str__(self):
        return self.title or self.youtube_id

    def get_absolute_url(self):
        return reverse('agadmator:video_detail', args=[self.youtube_id])

    def modify(self, save=True):
        # agadmator line separator
        self.description = re.sub(r'[-]{5,}', '---', self.description)
        if save:
            self.save()

    def store_names(self):

        white, black = self.extracted_players

        if not self.data.get('white'):
            self.data['white'] = {
                'name': white,
                'slug': slugify(white),
            }

        if not self.data.get('black'):
            self.data['black'] = {
                'name': black,
                'slug': slugify(black)
            }

        self.save(update_fields=['data'])

    @property
    def thumbnail_default(self):
        return f'https://i.ytimg.com/vi/{self.youtube_id}/default.jpg'

    @property
    def thumbnail_medium(self):
        return f'https://i.ytimg.com/vi/{self.youtube_id}/mqdefault.jpg'

    @property
    def thumbnail_high(self):
        return f'https://i.ytimg.com/vi/{self.youtube_id}/hqdefault.jpg'

    @cached_property
    def extracted_pgn(self):
        return extract_pgn(self.description)

    @cached_property
    def extracted_players(self):
        return extract_players(self.description)

    @cached_property
    def extracted_moves(self):
        numbers = re.findall(r'(\d+)\.', self.extracted_pgn)
        if numbers:
            return numbers[-1]
        return None


    @cached_property
    def pgn(self):
        chessgames_pgn = self.data.get('chessgames_pgn')
        return chessgames_pgn if chessgames_pgn else self.extracted_pgn

    @cached_property
    def normalized_pgn(self):
        if not self.game:
            return ''
        exporter = StringExporter(
            columns=None, headers=False, comments=False, variations=False
        )
        return self.game.accept(exporter).rstrip('* ')

    @cached_property
    def fen_list(self):
        if not self.game:
            return ''
        exporter = FenExporter()
        positions = self.game.accept(exporter)
        positions.append(self.game.end().board().fen())
        return positions

    @cached_property
    def pgn_markup(self):
        if not self.game:
            return ''
        exporter = MarkupExporter()
        return self.game.accept(exporter)

    @cached_property
    def game(self):
        if not self.pgn:
            return None
        return read_game(StringIO(self.pgn))

    @property
    def chessgames_similar_game_search_url(self):

        player, player2 = self.extracted_players

        params = {
            'yearcomp': 'exactly',
            'year': '',
            'playercomp': 'either',
            'player': player,
            'player2': player2,
            'movescomp': 'exactly',
            'moves': self.extracted_moves,
        }

        return 'http://www.chessgames.com/perl/chess.pl?' + urlencode(params)

    class Meta:
        verbose_name = 'Video'
        verbose_name_plural = 'Videos'
        indexes = [
            GinIndex(fields=['search_vector'])
        ]

    def tags(self):
        tags = []

        white, black = self.extracted_players

        if white:
            tags.append({
                'link': reverse('agadmator:player_detail', args=[slugify(white)]),
                'text': white
            })
        if black:
            tags.append({
                'link': reverse('agadmator:player_detail', args=[slugify(black)]),
                'text': black
            })

        # if self.game.tournament:
        #     tags.append({
        #         'link': reverse('agadmator:tournament_detail', args=[self.game.tournament_id]),
        #         'text': self.game.tournament.name
        #     })
        #     tags.append(f't: {self.game.tournament.name}')

        return tags
