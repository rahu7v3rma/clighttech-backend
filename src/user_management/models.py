from django.contrib.auth import get_user_model
from django.contrib.auth.models import UserManager
from django.contrib.auth.tokens import default_token_generator
from django.db import models

from user_profile.models import Profile

# user model used for auth
UserModel = get_user_model()

# token generator
TOKEN_GENERATOR = default_token_generator


class ResetPasswordToken(models.Model):
    class Meta:
        verbose_name = 'Password Reset Token'
        verbose_name_plural = 'Password Reset Tokens'

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        UserModel,
        related_name='password_reset_tokens',
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    token = models.CharField(max_length=255, db_index=True, unique=True)
    ip_address = models.GenericIPAddressField(
        default='', blank=True, null=True
    )
    user_agent = models.CharField(max_length=256, default='', blank=True)

    def _generate_token(self):
        return TOKEN_GENERATOR.make_token(self.user)

    def verify(self):
        return TOKEN_GENERATOR.check_token(self.user, self.token)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = self._generate_token()

        return super().save(*args, **kwargs)


class CustomerManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_staff=False)


class Customer(UserModel):
    objects = CustomerManager()

    def save(self, *args, **kwargs):
        created = not self.pk
        super().save(*args, **kwargs)
        if created:
            Profile.objects.create(user=self)

    class Meta:
        proxy = True


class AdminManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_staff=True)


class Admin(UserModel):
    objects = AdminManager()

    class Meta:
        proxy = True
