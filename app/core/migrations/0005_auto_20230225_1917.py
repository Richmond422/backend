# Generated by Django 3.2.18 on 2023-02-25 19:17

import core.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20230224_2300'),
    ]

    operations = [
        migrations.RenameField(
            model_name='imagerecord',
            old_name='image',
            new_name='image_ir',
        ),
        migrations.RenameField(
            model_name='location',
            old_name='path',
            new_name='path_id',
        ),
        migrations.RemoveField(
            model_name='hotspot',
            name='location',
        ),
        migrations.RemoveField(
            model_name='imagerecord',
            name='type',
        ),
        migrations.AddField(
            model_name='hotspot',
            name='record_id',
            field=models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, to='core.imagerecord'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='imagerecord',
            name='image_rgb',
            field=models.ImageField(null=True, upload_to=core.models.recipe_image_file_path),
        ),
    ]
