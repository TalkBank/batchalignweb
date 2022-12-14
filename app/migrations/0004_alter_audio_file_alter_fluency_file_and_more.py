# Generated by Django 4.0 on 2022-07-31 23:49

import app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_job_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audio',
            name='file',
            field=models.FileField(upload_to=app.models.file_path),
        ),
        migrations.AlterField(
            model_name='fluency',
            name='file',
            field=models.FileField(upload_to=app.models.file_path),
        ),
        migrations.AlterField(
            model_name='transcript',
            name='file',
            field=models.FileField(upload_to=app.models.file_path),
        ),
    ]
