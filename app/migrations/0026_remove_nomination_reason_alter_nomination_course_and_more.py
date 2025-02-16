# Generated by Django 5.1.3 on 2025-02-05 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0025_alter_nomination_course_alter_nomination_department_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nomination',
            name='reason',
        ),
        migrations.AlterField(
            model_name='nomination',
            name='course',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='nomination',
            name='department',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='nomination',
            name='email',
            field=models.EmailField(max_length=100),
        ),
        migrations.AlterField(
            model_name='nomination',
            name='name',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='nomination',
            name='phoneno',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='nomination',
            name='regno',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='nomination',
            name='status',
            field=models.CharField(max_length=20),
        ),
    ]
