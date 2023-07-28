from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import Group


class Profile(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE, primary_key=True
    )
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
