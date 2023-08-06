from django.contrib import admin
from django.utils.safestring import mark_safe

from .utils import new_session
from .models import Video, Message
from .chessgames import get_best_match, update_video
from pprint import pformat


class VideoAdmin(admin.ModelAdmin):
    date_hierarchy = 'time_published'
    list_display = [
        'id',
        'title',
        'time_published',
        'white_name',
        'black_name',
        'chessgames_id',
        'tournament_id',
        'stream',
        'engine',
        'ignore',
        'error',

    ]
    list_filter = [
        'ignore',
        'stream',
        'engine',
        'error',
    ]
    list_editable = [

        'ignore',
        'stream',
        'engine',
    ]
    search_fields = [
        'id',
        'title',
        'description',
        'youtube_id',
        'white_name',
        'black_name',
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


class MessageAdmin(admin.ModelAdmin):
    list_display = ['time_created', 'name', 'email', 'content']
    date_hierarchy = 'time_created'


admin.site.register(Video, VideoAdmin)
admin.site.register(Message, MessageAdmin)
