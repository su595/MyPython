# Generated by Django 3.2.7 on 2021-09-30 22:12

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0004_auto_20210930_2344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bike',
            name='lastContactWithServer',
            field=models.DateTimeField(verbose_name=datetime.datetime(2021, 9, 30, 22, 12, 6, 947861, tzinfo=utc)),
        ),
    ]
