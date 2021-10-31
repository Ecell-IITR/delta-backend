# Generated by Django 3.2.5 on 2021-10-30 17:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('utilities', '0019_auto_20211030_2304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skill',
            name='name',
            field=models.CharField(help_text='Type the skill name you want to add', max_length=255, unique=True, verbose_name='Skill'),
        ),
        migrations.AlterField(
            model_name='type',
            name='name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='utilities.skill', to_field='name'),
        ),
    ]
