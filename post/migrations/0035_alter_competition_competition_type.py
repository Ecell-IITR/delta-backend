# Generated by Django 3.2.6 on 2021-09-11 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("post", "0034_auto_20200620_1003"),
    ]

    operations = [
        migrations.AlterField(
            model_name="competition",
            name="competition_type",
            field=models.CharField(
                choices=[("1", "Online"), ("2", "Onspot")],
                default="1",
                max_length=255,
                verbose_name="Competition type",
            ),
        ),
    ]
