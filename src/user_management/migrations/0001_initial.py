# Generated by Django 4.0.5 on 2022-06-07 13:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ResetPasswordToken',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                (
                    'token',
                    models.CharField(
                        db_index=True, max_length=255, unique=True
                    ),
                ),
                (
                    'ip_address',
                    models.GenericIPAddressField(
                        blank=True, default='', null=True
                    ),
                ),
                (
                    'user_agent',
                    models.CharField(blank=True, default='', max_length=256),
                ),
                (
                    'user',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='password_reset_tokens',
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                'verbose_name': 'Password Reset Token',
                'verbose_name_plural': 'Password Reset Tokens',
            },
        ),
    ]
