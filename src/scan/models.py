from django.db import models
from django.contrib.auth import get_user_model
from lib.models import BaseModel


class RawData(BaseModel):
    EYE_CHOICES = [(0, 'left'), (1, 'right')]
    MODE_CHOICES = [(0, 'Fixation mode'), (1, 'Saccade tracking mode 3')]
    hd5_url = models.TextField()
    video_url = models.TextField(default=None, null=True, blank=True)
    eye = models.IntegerField(
        choices=EYE_CHOICES, default=None, null=True, blank=True
    )
    mode = models.IntegerField(
        choices=MODE_CHOICES, default=None, null=True, blank=True
    )
    proceed_at = models.DateTimeField(default=None, null=True, blank=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
