# Generated by Django 3.2.8 on 2022-06-02 15:55

import datetime
from django.db import migrations, models
import django.utils.timezone
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20220602_1526'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='affiliation',
            field=models.CharField(default=django.utils.timezone.now, max_length=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='email',
            field=models.EmailField(default=django.utils.timezone.now, max_length=254),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='code',
            name='heure',
            field=models.TimeField(verbose_name=datetime.datetime(2022, 6, 2, 15, 54, 26, 943365, tzinfo=utc)),
        ),
    ]