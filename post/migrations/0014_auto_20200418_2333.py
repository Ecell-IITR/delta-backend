# Generated by Django 2.1.7 on 2020-04-18 23:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0013_appliedpostentries'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appliedpostentries',
            name='post_object_id',
        ),
        migrations.AddField(
            model_name='appliedpostentries',
            name='entity_object_id',
            field=models.PositiveIntegerField(default=1, verbose_name='Post Object Id'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='appliedpostentries',
            name='post_content_type',
            field=models.ForeignKey(limit_choices_to=models.Q(models.Q(('app_label', 'post'), ('model', 'internship')), models.Q(('app_label', 'post'), ('model', 'competition')), models.Q(('app_label', 'post'), ('model', 'project')), _connector='OR'), on_delete=django.db.models.deletion.CASCADE, related_name='applied_post_entries_post', to='contenttypes.ContentType'),
        ),
    ]
