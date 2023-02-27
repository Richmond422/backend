# Generated by Django 3.2.18 on 2023-02-27 04:22

import core.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x', models.FloatField()),
                ('y', models.FloatField()),
                ('path_id', models.IntegerField(default=-1)),
            ],
        ),
        migrations.CreateModel(
            name='ImageRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('image_ir', models.ImageField(null=True, upload_to=core.models.recipe_image_file_path)),
                ('image_rgb', models.ImageField(null=True, upload_to=core.models.recipe_image_file_path)),
                ('image_masked', models.ImageField(null=True, upload_to=core.models.recipe_image_file_path)),
                ('is_hotspot', models.BooleanField(default=False)),
                ('is_classified', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[('Viewed', 'Viewed'), ('Visited', 'Visited'), ('Dismissed', 'Dismissed'), ('Not viewed', 'Notviewed')], default='Viewed', max_length=20)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.location')),
            ],
        ),
    ]
