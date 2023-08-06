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
    try:
        get_best_match(video)
    except Exception as e:
        video.error = True
        video.error_message = str(e)
        video.save()
        return

    update_video(video)


def update_search_vectors():
    with connection.cursor() as cursor:
        cursor.execute("""
        UPDATE agadmator_video v
        SET search_vector = document.vector
        FROM (
        SELECT id,
        setweight(to_tsvector('simple', coalesce(title, '')),'A') ||
        setweight(to_tsvector('simple', coalesce(white_name,'') || ' ' || coalesce(black_name,'')), 'A') ||
        -- setweight(to_tsvector('simple', coalesce(description, '')), 'C') ||
        setweight(to_tsvector('simple', coalesce(array_to_string(ARRAY( SELECT jsonb_array_elements_text(data->'tags')),' '), '')),'C') AS vector
        FROM agadmator_video
        ) document
        WHERE v.id = document.id
            
        """)


def find_best_match_and_update_eligible_videos():
    session = new_session()
    videos = Video.objects.filter(
        ignore=False,
        stream=False,
        engine=False,
        chessgames_id=None,
    ).order_by('-time_published')

    for v in videos:
        w, b = v.extracted_players
        if w == "" or b == "":
            v.ignore = True
            v.error = 'Could not extract players'
            v.save()
            continue
        result = False
        try:
            result = get_best_match(v, session=session)
        except Exception as e:
            result = False
            v.error = True
            v.error_message = str(e)
            v.save()
            continue
        finally:
            time.sleep(1)
        if result:
            update_video(v, session=session)


def vaccuum_data():
    for vid in Video.objects.all():
        data = vid.data
        delattr(data, 'tournament')
        delattr(data, 'white')
        delattr(data, 'black')
        delattr(data, 'year')

        vid.data = data
        vid.save()


# this is not used for anything yet
# but can be used in postgres query when
# updating search vectors
TAG_BLACKLIST = [
    'agadmator',
    'chess',
    'best',
    'channel',
    'youtube',
    'vs',
    'match',
    'game'
]