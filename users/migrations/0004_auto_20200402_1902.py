# Generated by Django 2.1.7 on 2020-04-02 19:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20200402_1900'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sociallink',
            name='website',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='utilities.Website'),
        ),
    ]
