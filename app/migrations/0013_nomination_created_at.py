# Generated by Django 5.1.3 on 2024-12-07 05:10

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_vote'),
    ]

    operations = [
        migrations.AddField(
            model_name='nomination',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
