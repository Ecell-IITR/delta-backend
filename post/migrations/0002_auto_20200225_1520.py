# Generated by Django 2.2.10 on 2020-02-25 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='internship',
            name='work_type',
            field=models.CharField(choices=[('Part time', 'Part time'), ('Full time', 'Full time')], default='part time', max_length=255, verbose_name='Type of Work'),
        ),
    ]