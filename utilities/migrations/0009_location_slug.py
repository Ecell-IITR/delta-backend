# Generated by Django 2.1.7 on 2020-05-11 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("utilities", "0008_auto_20200511_0431"),
    ]

    operations = [
        migrations.AddField(
            model_name="location",
            name="slug",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
