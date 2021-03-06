# Generated by Django 3.1.6 on 2021-02-19 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kover', '0004_auto_20210219_0214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='people',
            name='people_img',
            field=models.URLField(blank=True, verbose_name='인물사진url'),
        ),
        migrations.AlterField(
            model_name='show',
            name='show_poster',
            field=models.URLField(blank=True, verbose_name='공연 포스터 url'),
        ),
    ]
