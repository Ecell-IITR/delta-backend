# Generated by Django 2.1.7 on 2020-04-15 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20200408_2211'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sociallink',
            options={'verbose_name_plural': 'Socila Links'},
        ),
        migrations.AlterField(
            model_name='student',
            name='social_links',
            field=models.ManyToManyField(blank=True, related_name='social_links', to='users.SocialLink'),
        ),
    ]
