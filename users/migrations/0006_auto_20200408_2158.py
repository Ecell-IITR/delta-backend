# Generated by Django 2.1.7 on 2020-04-08 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20200404_0835'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='is_company',
        ),
        migrations.RemoveField(
            model_name='person',
            name='is_student',
        ),
        migrations.AddField(
            model_name='person',
            name='role_type',
            field=models.CharField(choices=[('Company', 'Company'), ('Student', 'Student')], default='Student', max_length=255, verbose_name='User role'),
        ),
    ]
