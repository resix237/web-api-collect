# Generated by Django 4.0.3 on 2022-04-12 10:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='tags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='images_tags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tags_value', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='api_collect.tags')),
            ],
        ),
        migrations.CreateModel(
            name='images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.CharField(max_length=200)),
                ('count', models.IntegerField(null=True)),
                ('his_tags', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='api_collect.tags')),
                ('list_tags', models.ManyToManyField(to='api_collect.images_tags')),
            ],
        ),
    ]
