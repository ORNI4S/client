# Generated by Django 4.1.4 on 2023-04-04 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_userdata_used_account_alter_userdata_account_count'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userdata',
            old_name='used_account',
            new_name='account_used',
        ),
        migrations.RemoveField(
            model_name='userdata',
            name='eshterak',
        ),
        migrations.AddField(
            model_name='userdata',
            name='subscription',
            field=models.DateField(default=None),
        ),
    ]