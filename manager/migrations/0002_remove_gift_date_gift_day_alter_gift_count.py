# Generated by Django 4.1.4 on 2023-04-04 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gift',
            name='date',
        ),
        migrations.AddField(
            model_name='gift',
            name='day',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='gift',
            name='count',
            field=models.IntegerField(default=0),
        ),
    ]