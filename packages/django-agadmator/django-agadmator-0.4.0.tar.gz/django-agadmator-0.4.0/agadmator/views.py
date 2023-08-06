from django.http import Http404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.db.models.aggregates import Count
# Create your views here.
from django.db import connection
from django.db.models import Q, F
from django.contrib.postgres.search import SearchQuery, SearchRank
from .models import Video, Message
from django.contrib.messages.views import SuccessMessageMixin

from collections import namedtuple


def fetchall(cursor):
    """Return all rows from a cursor as a namedtuple"""
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]


class IndexView(generic.TemplateView):
    template_name = 'agadmator/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['videos'] = (
            Video.objects.all().order_by('-time_published')[:12]
        )

        with connection.cursor() as cursor:
            cursor.execute("""
            SELECT count(*) AS count,
                   name,
                   slug,
                   row_number() OVER (ORDER BY count(*) DESC, name) AS video_ix,
                   row_number() OVER (ORDER BY name) AS name_ix
            FROM (SELECT black_name AS name, black_slug AS slug FROM agadmator_video
                  UNION ALL
                  SELECT white_name AS name, white_slug AS slug FROM agadmator_video) t
            WHERE name != ''
            GROUP BY name, slug
            ORDER BY count DESC
            """)
            context['players'] = fetchall(cursor)

        with connection.cursor() as cursor:
            cursor.execute("""
            SELECT
                count(*) AS count,
                tournament_name AS name,
                tournament_id AS id,
                row_number() OVER (ORDER BY tournament_name) AS name_ix,
                row_number() OVER (ORDER BY count(*) DESC ) AS videos_ix
            FROM agadmator_video
            WHERE tournament_id NOTNULL
            GROUP BY tournament_id, tournament_name
            ORDER BY count DESC;
            """)

            context['tournaments'] = fetchall(cursor)

        with connection.cursor() as cursor:
            cursor.execute(
                """SELECT year AS year,
                    count(*) AS num_videos
                    FROM agadmator_video
        WHERE year NOTNULL
        GROUP BY year
        ORDER BY year""")
            context['years'] = fetchall(cursor)

        with connection.cursor() as cursor:
            cursor.execute(
                """SELECT to_char(time_published, 'YYYY-MM' ) AS month, count(*) AS num_videos
                FROM agadmator_video
                GROUP BY month
                ORDER BY month DESC""")
            context['published_months'] = fetchall(cursor)

        return context


class VideoListView(generic.ListView):
    model = Video
    paginate_by = 21
    template_name = 'agadmator/video_list.html'
    context_object_name = 'videos'
    ordering = ['-time_published']

    def get_queryset(self):
        qs = super().get_queryset()

        if self.request.GET.get('unknown'):
            qs = qs.filter(chessgames_id=None)

        q = self.request.GET.get('q')
        if q:
            query = SearchQuery(q, config='simple')
            qs = qs.filter(search_vector=query).annotate(rank=SearchRank(F('search_vector'), query)).order_by('-rank')

        return qs


class VideoDetailView(generic.DetailView):
    template_name = 'agadmator/video_detail.html'
    model = Video
    context_object_name = 'video'
    slug_field = 'youtube_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PlayerDetailView(generic.TemplateView):
    template_name = 'agadmator/player_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        id_or_slug = self.kwargs.get('id_or_slug')
        slug = ''
        chessgames_id = None
        try:
            chessgames_id = int(id_or_slug)
        except ValueError:
            slug = id_or_slug

        videos = Video.objects.all().order_by('-time_published')

        if chessgames_id:
            videos = videos.filter(
                Q(data__white__chessgames_id=chessgames_id) | Q(data__black__chessgames_id=chessgames_id)
            )
            context['chessgames_id'] = chessgames_id
        elif slug:
            videos = videos.filter(
                Q(white_slug=slug) | Q(black_slug=slug)
            )

        context['videos'] = videos

        name = ''
        for v in videos:
            for side in ['black', 'white']:
                if getattr(v, f'{side}_slug') == slug:
                    name = getattr(v, f'{side}_name')
                    break

        context['name'] = name
        return context


class TournamentDetailView(generic.TemplateView):
    template_name = 'agadmator/tournament_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        chessgames_id = self.kwargs.get('chessgames_id')

        videos = Video.objects.filter(
            tournament_id=chessgames_id
        ).order_by('-time_published')

        if not videos:
            raise Http404()

        context['videos'] = videos
        context['name'] = videos[0].tournament_name
        context['chessgames_id'] = chessgames_id
        return context


class AboutView(generic.TemplateView):
    template_name = 'agadmator/about.html'


class YearDetailView(generic.TemplateView):
    template_name = 'agadmator/year_detail.html'

    def get_context_data(self, **kwargs):
        year = self.kwargs.get('year')
        context = super().get_context_data(**kwargs)
        context['videos'] = Video.objects.filter(year=year)
        return context


class PublishedMonthDetailView(generic.TemplateView):
    template_name = 'agadmator/published_month_detail.html'

    def get_context_data(self, **kwargs):
        year_month = self.kwargs.get('year_month')
        year, month = year_month.split('-')
        context = super().get_context_data(**kwargs)
        context['videos'] = Video.objects.filter(
            time_published__year=year,
            time_published__month=month
        )
        return context


class ContactView(SuccessMessageMixin, generic.CreateView):
    model = Message
    template_name = 'agadmator/contact.html'
    fields = [
        'name',
        'email',
        'content',
    ]
    success_url = reverse_lazy('agadmator:index')
    success_message = 'Your message has been received.'
