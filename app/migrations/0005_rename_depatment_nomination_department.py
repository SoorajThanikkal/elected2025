# Generated by Django 5.1.3 on 2024-11-23 06:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_nomination'),
    ]

    operations = [
        migrations.RenameField(
            model_name='nomination',
            old_name='depatment',
            new_name='department',
        ),
    ]
