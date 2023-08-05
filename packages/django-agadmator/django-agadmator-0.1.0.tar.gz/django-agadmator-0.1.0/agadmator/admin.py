from django.contrib import admin
from django.utils.safestring import mark_safe

from .utils import new_session
from . import models
from .chessgames import get_best_match, update_video
from pprint import pformat


class VideoAdmin(admin.ModelAdmin):
    date_hierarchy = 'time_published'
    list_display = [
        'id',
        'title',

        # 'time_updated',
        # 'time_published',
        'extracted_players',
        'chessgames_id',
        # 'extracted_moves',
        # 'possible_games',
        # 'sim_ratios',
        #  'auto_imported',
        #  'stream',
        #  'engine',
        #  'possible_games',
    ]
    list_filter = [

    ]
    list_editable = [
        # 'game_id',
        #  'series',
        #  'stream',
        #    'engine',
    ]
    search_fields = [
        'id',
        'title',
        'description',
    ]
    ordering = [
        '-time_published'
    ]
    readonly_fields = [
        'time_updated',
        'extracted_moves',
        'extracted_players',
        'chessgames_similar_game_search_url',
        'data_pre',
        'search_vector',
    ]

    actions = [
        'inline_sync_with_api',
        'schedule_sync_with_api',
        'get_best_match',
        'update_from_chessgames',
        'match_on_similarity',
    ]

    # class Media:
    #     js = (
    #         'agadmator/chessgames.js',
    #     )

    def get_best_match(self, r, qs):
        session = new_session()
        success = 0
        for obj in qs:
            result_id = get_best_match(obj, session=session)
            if result_id:
                success += 1
            update_video(obj, session=session)
        self.message_user(r, f'Auto match: Total {len(qs)}, Success {success}')

    def match_on_similarity(self, r, qs):
        success = 0
        for obj in qs:
            result = obj.match_on_possible_game_similarity()
            if result:
                success += 1
        self.message_user(r, f'Similarity matching: Total {len(qs)}, Success {success}')

    def update_from_chessgames(self, r, qs):
        session = new_session()
        for obj in qs:
            update_video(obj, session=session)
        self.message_user(r, f'Update: Total {len(qs)}')

    def data_pre(self, obj):
        return mark_safe(f'<pre>{pformat(obj.data, indent=2)}</pre>')

admin.site.register(models.Video, VideoAdmin)
