# Generated by Django 2.1.7 on 2020-04-18 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0011_auto_20200417_2215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='internship',
            name='work_type',
            field=models.CharField(choices=[('Full time', 'Full time'), ('Part time', 'Part time')], default='part time', max_length=255, verbose_name='Type of Work'),
        ),
    ]
