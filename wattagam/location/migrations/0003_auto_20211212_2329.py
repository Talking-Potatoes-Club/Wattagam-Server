# Generated by Django 3.2.8 on 2021-12-12 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0002_picture_contents'),
    ]

    operations = [
        migrations.AddField(
            model_name='picture',
            name='origin_x_location',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='picture',
            name='origin_y_location',
            field=models.FloatField(default=0.0),
        ),
    ]
