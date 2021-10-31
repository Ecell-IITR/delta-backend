# Generated by Django 2.1.7 on 2020-03-31 19:23

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import utilities.models.website


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Branch",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "name",
                    models.CharField(
                        help_text="Type the branch name to be added..",
                        max_length=255,
                        verbose_name="Branch",
                    ),
                ),
                (
                    "code",
                    models.CharField(
                        blank=True,
                        max_length=255,
                        null=True,
                        verbose_name="Branch Code",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Branch",
            },
        ),
        migrations.CreateModel(
            name="Country",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "name",
                    models.CharField(
                        default="India", max_length=255, verbose_name="Country"
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Country",
            },
        ),
        migrations.CreateModel(
            name="Location",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "name",
                    models.CharField(
                        help_text="Type the Location name to be added..",
                        max_length=255,
                        verbose_name="Location",
                    ),
                ),
                ("pin_code", models.IntegerField(unique=True, verbose_name="Pincode")),
                (
                    "country",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="utilities.Country",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Location",
            },
        ),
        migrations.CreateModel(
            name="Skill",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "name",
                    models.CharField(
                        help_text="Type the skill name you want to add",
                        max_length=255,
                        verbose_name="Skill",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Skill",
            },
        ),
        migrations.CreateModel(
            name="State",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=255, verbose_name="State")),
                (
                    "country",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="state",
                        to="utilities.Country",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "State",
            },
        ),
        migrations.CreateModel(
            name="Website",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=155, verbose_name="Website Name")),
                (
                    "website_url",
                    models.URLField(
                        blank=True,
                        null=True,
                        validators=[django.core.validators.URLValidator],
                    ),
                ),
                (
                    "website_logo",
                    models.ImageField(
                        default="null",
                        upload_to="social_link_logo/",
                        validators=[utilities.models.website.validate_image],
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "websites",
            },
        ),
        migrations.AddField(
            model_name="location",
            name="state",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE, to="utilities.State"
            ),
        ),
    ]
