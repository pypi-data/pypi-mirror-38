import feedparser
from celery import shared_task
from celery.utils.log import get_task_logger
from django.utils.timezone import now
from datetime import timedelta

from .models import Video
from agadmator import YOUTUBE_CHANNEL_ID
from .chessgames import get_best_match, update_video
from django.db import connection
from .utils import new_session
import time
logger = get_task_logger(__name__)


@shared_task
def sync_channel_rss_feed():
    rss_url = f'https://www.youtube.com/feeds/videos.xml?channel_id={YOUTUBE_CHANNEL_ID}'

    num_created = 0

    for entry in feedparser.parse(rss_url).entries:
        youtube_id = entry.yt_videoid
        video, created = Video.objects.get_or_create(
            youtube_id=youtube_id,
            defaults={
                'title': entry.title,
                'time_published': entry.published,
                'description': entry.summary
            }
        )
        if created:
            num_created += 1
            video.store_names()
    logger.info(f'Number of videos created: {num_created}')


@shared_task
def sync_channel_and_schedule_match_on_chessgames():
    logger.info('Updating channels over RSS')
    sync_channel_rss_feed()

    new_videos = Video.objects.filter(time_updated__gt=now() - timedelta(minutes=10))

    logger.info(f'New videos: {len(new_videos)}')

    for video in new_videos:
        find_best_chessgames_match_for_video.delay(video.id)

    if len(new_videos) > 0:
        update_search_vectors()
    logger.info('Done')


@shared_task
def find_best_chessgames_match_for_video(video_id):
    video = Video.objects.get(id=video_id)
    game_id = get_best_match(video)
    if game_id:
        video.data['chessgame_id'] = game_id

    video.data['chessgames_match_time'] = now()
    video.save(update_fields=['data'])
    update_video(video)


@shared_task
def find_best_matches_for_all_videos_not_checked_yet():
    videos = Video.objects.filter(data__chessgames_match_time=None)
    for video in videos:
        find_best_chessgames_match_for_video.delay(video.id)
    logger.info('Scheduled {} games for auto matching.'.format(len(videos)))



def update_search_vectors():

    with connection.cursor() as cursor:

        cursor.execute("""
        update agadmator_video v
        set search_vector = document.vector
        from (
        SELECT id,
        setweight(to_tsvector('simple', coalesce(title, '')),'A') ||
        setweight(to_tsvector('simple', coalesce(data->'white'->>'name','') || ' ' || coalesce(data->'black'->>'name','')), 'A') ||
        setweight(to_tsvector('simple', coalesce(description, '')), 'C') ||
        setweight(to_tsvector('simple', coalesce(array_to_string(ARRAY( SELECT jsonb_array_elements_text(data->'tags')),' '), '')),'A') AS vector
        FROM agadmator_video
        ) document
        where v.id = document.id
            
        """)


def find_best_match_and_update_eligible_videos():

    session = new_session()
    videos = Video.objects.filter(
        ignore=False,
        stream=False,
        engine=False,
        chessgames_id=None,
    )

    for v in videos:
        result = False
        try:
            result = get_best_match(v, session=session)
        except Exception as e:
            result = False
            v.error = str(e)
            v.ignore = True
            v.save()
            continue
        finally:
            time.sleep(1)
        if result:
            update_video(v, session=session)
