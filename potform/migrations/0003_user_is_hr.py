# Generated by Django 2.2.17 on 2021-03-07 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('potform', '0002_auto_20210307_1303'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_hr',
            field=models.BooleanField(default=False),
        ),
    ]
