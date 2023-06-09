# Generated by Django 4.1.4 on 2023-04-04 14:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0004_alter_userdata_subscription_giftuser'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAccounts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fpass', models.CharField(default=None, max_length=200)),
                ('second', models.PositiveIntegerField(default=180)),
                ('collected_gold', models.CharField(default=None, max_length=200)),
                ('player_gold', models.CharField(default=None, max_length=200)),
                ('gold_collection_allowed', models.CharField(default=None, max_length=200)),
                ('gold_collection_allowed_at', models.CharField(default=None, max_length=200)),
                ('gold_collection_extraction', models.CharField(default=None, max_length=200)),
                ('last_gold_collect_at', models.CharField(default=None, max_length=200)),
                ('needs_captcha', models.CharField(default=None, max_length=200)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accounts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
