# Generated by Django 2.1.7 on 2020-06-03 14:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('utilities', '0010_auto_20200603_1356'),
        ('post', '0025_auto_20200511_0441'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='competition',
            name='required_skill',
        ),
        migrations.RemoveField(
            model_name='internship',
            name='duration',
        ),
        migrations.RemoveField(
            model_name='internship',
            name='required_skill',
        ),
        migrations.RemoveField(
            model_name='project',
            name='required_skill',
        ),
        migrations.AddField(
            model_name='competition',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='utilities.Location'),
        ),
        migrations.AddField(
            model_name='competition',
            name='required_skills',
            field=models.ManyToManyField(blank=True, related_name='required_skills_competitions', to='utilities.Skill', verbose_name='Required skill set'),
        ),
        migrations.AddField(
            model_name='internship',
            name='duration_unit',
            field=models.CharField(blank=True, choices=[(4, 'year'), (2, 'week'), (1, 'day'), (3, 'month')], default=3, max_length=255),
        ),
        migrations.AddField(
            model_name='internship',
            name='duration_value',
            field=models.IntegerField(blank=True, null=True, verbose_name='Duration'),
        ),
        migrations.AddField(
            model_name='internship',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='utilities.Location'),
        ),
        migrations.AddField(
            model_name='internship',
            name='required_skills',
            field=models.ManyToManyField(blank=True, related_name='required_skills_internships', to='utilities.Skill', verbose_name='Required skill set'),
        ),
        migrations.AddField(
            model_name='project',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='utilities.Location'),
        ),
        migrations.AddField(
            model_name='project',
            name='required_skills',
            field=models.ManyToManyField(blank=True, related_name='required_skills_project', to='utilities.Skill', verbose_name='Required skill set'),
        ),
        migrations.AlterField(
            model_name='competition',
            name='competition_type',
            field=models.CharField(choices=[(1, 'Online'), (2, 'Onspot')], default=1, max_length=255, verbose_name='Competition type'),
        ),
        migrations.AlterField(
            model_name='internship',
            name='stipend',
            field=models.BigIntegerField(blank=True, help_text='Stipend should be in rupees.', verbose_name='Stipend'),
        ),
        migrations.AlterField(
            model_name='internship',
            name='work_type',
            field=models.CharField(choices=[(2, 'Part time'), (1, 'Full time')], default=2, max_length=255, verbose_name='Type of Work'),
        ),
    ]
