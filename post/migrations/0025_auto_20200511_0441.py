# Generated by Django 2.1.7 on 2020-05-11 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("post", "0024_auto_20200511_0427"),
    ]

    operations = [
        migrations.AlterField(
            model_name="internship",
            name="work_type",
            field=models.CharField(
                choices=[("Part time", "Part time"), ("Full time", "Full time")],
                default="part time",
                max_length=255,
                verbose_name="Type of Work",
            ),
        ),
    ]
