# agadmator

This is a Django project that pulls videos from YouTube using
either the API or RSS.

### requirements

- postgres

### install

1. `pip install django-agadmator`
1. add `django.contrib.humanize` to `INSTALLED_APPS`
1. add `agadmator` to `INSTALLED_APPS`

### getting data channel data

1. `youtube_dl -J UUL5YbN5WLFD8dLIegT5QAbA > data.json`
1. `python manage.py import_initial_playlist_dump data.json`

### periodic tasks

Add the following tasks to celery beat schedule:

- `agadmator.tasks.sync_channel_and_schedule_match_on_chessgames` ()

### todo

- task to update tags with youtube_dl
- more robust date parsing from chessgames pgn if `?` in date string
- clean search vectors
- related videos
- fix russian names parsing -> ...vsky causes regex to split in surname