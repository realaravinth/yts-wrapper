# Generated by Django 3.0 on 2020-05-24 10:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yify', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='downloading',
            name='downloaded_on',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 24, 15, 59, 21, 900501)),
        ),
    ]