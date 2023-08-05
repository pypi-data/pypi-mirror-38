import logging



from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from .models import Video

logger = logging.getLogger(__name__)