from django.urls import path
from agadmator import views

urlpatterns = [
    path('videos/', views.VideoListView.as_view(), name='video_list'),
    path('videos/<str:slug>/', views.VideoDetailView.as_view(), name='video_detail'),
    path('player/<str:id_or_slug>/', views.PlayerDetailView.as_view(), name='player_detail'),
    path('tournament/<int:pk>/', views.TournamentDetailView.as_view(), name='tournament_detail'),
    path('year/<int:year>/', views.YearDetailView.as_view(), name='year_detail'),
    path('published/<year_month>/', views.PublishedMonthDetailView.as_view(), name='published_month_detail'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('', views.IndexView.as_view())
]

app_name = 'agadmator'