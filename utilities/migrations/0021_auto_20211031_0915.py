# Generated by Django 3.2.5 on 2021-10-31 03:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('utilities', '0020_auto_20211030_2305'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='type',
            name='name',
        ),
        migrations.AddField(
            model_name='skill',
            name='type',
            field=models.ForeignKey(default='tech', on_delete=django.db.models.deletion.DO_NOTHING, to='utilities.type', to_field='type'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='skill',
            name='name',
            field=models.CharField(help_text='Type the skill name you want to add', max_length=255, verbose_name='Skill'),
        ),
        migrations.AlterField(
            model_name='type',
            name='type',
            field=models.CharField(default='tech', help_text='Type of skill you want to add', max_length=255, unique='true'),
        ),
    ]
