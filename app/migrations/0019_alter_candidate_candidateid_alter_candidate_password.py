# Generated by Django 5.1.4 on 2025-01-01 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_alter_candidate_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='candidateid',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='password',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
