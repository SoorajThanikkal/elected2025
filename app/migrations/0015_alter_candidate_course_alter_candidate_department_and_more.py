# Generated by Django 5.1.4 on 2024-12-26 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_notification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='course',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='department',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='position',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
