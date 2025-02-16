# Generated by Django 5.1.3 on 2025-01-31 18:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0024_alter_nomination_course_alter_nomination_department_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nomination',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_nomination', to='app.student'),
        ),
        migrations.AlterField(
            model_name='nomination',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='department_nomination', to='app.student'),
        ),
        migrations.AlterField(
            model_name='nomination',
            name='email',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='email_nomination', to='app.student'),
        ),
        migrations.AlterField(
            model_name='nomination',
            name='name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='name_nomination', to='app.student'),
        ),
        migrations.AlterField(
            model_name='nomination',
            name='phoneno',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='phoneno_nomination', to='app.student'),
        ),
        migrations.AlterField(
            model_name='nomination',
            name='regno',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='regno_nomination', to='app.student'),
        ),
        migrations.AlterField(
            model_name='nomination',
            name='status',
            field=models.CharField(default='Pending', max_length=20),
        ),
    ]
