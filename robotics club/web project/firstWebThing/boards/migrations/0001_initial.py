# Generated by Django 3.2.7 on 2021-09-28 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('macAddress', models.TextField(max_length=12)),
                ('name', models.TextField(max_length=100)),
                ('isClamed', models.BooleanField()),
                ('inWifi', models.BooleanField()),
                ('size', models.TextField(max_length=1)),
                ('needsRepair', models.BooleanField()),
            ],
        ),
    ]
