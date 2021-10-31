# Generated by Django 2.1.7 on 2020-06-16 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0016_auto_20200504_2032"),
    ]

    operations = [
        migrations.AddField(
            model_name="company",
            name="company_name",
            field=models.CharField(
                blank=True, max_length=255, verbose_name="Company Name"
            ),
        ),
        migrations.AlterField(
            model_name="person",
            name="username",
            field=models.CharField(
                db_index=True, max_length=50, unique=True, verbose_name="Username"
            ),
        ),
    ]
