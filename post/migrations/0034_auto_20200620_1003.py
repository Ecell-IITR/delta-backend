# Generated by Django 2.1.7 on 2020-06-20 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0033_auto_20200619_1403'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competition',
            name='required_skills',
            field=models.ManyToManyField(blank=True, related_name='post_competition_required_skills', to='utilities.Skill', verbose_name='Required skill set'),
        ),
        migrations.AlterField(
            model_name='competition',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='post_competition_tags', to='utilities.Tag'),
        ),
        migrations.AlterField(
            model_name='internship',
            name='bookmarks',
            field=models.ManyToManyField(blank=True, related_name='post_internship_bookmarks', to='users.Student'),
        ),
        migrations.AlterField(
            model_name='internship',
            name='required_skills',
            field=models.ManyToManyField(blank=True, related_name='post_internship_required_skills', to='utilities.Skill', verbose_name='Required skill set'),
        ),
        migrations.AlterField(
            model_name='internship',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='post_internship_tags', to='utilities.Tag'),
        ),
        migrations.AlterField(
            model_name='project',
            name='bookmarks',
            field=models.ManyToManyField(blank=True, related_name='post_project_bookmarks', to='users.Student'),
        ),
        migrations.AlterField(
            model_name='project',
            name='required_skills',
            field=models.ManyToManyField(blank=True, related_name='post_project_required_skills', to='utilities.Skill', verbose_name='Required skill set'),
        ),
        migrations.AlterField(
            model_name='project',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='post_project_tags', to='utilities.Tag'),
        ),
    ]
