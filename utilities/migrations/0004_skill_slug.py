# Generated by Django 2.1.7 on 2020-04-25 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("utilities", "0003_tag"),
    ]

    operations = [
        migrations.AddField(
            model_name="skill",
            name="slug",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
