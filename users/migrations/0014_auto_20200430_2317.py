# Generated by Django 2.1.7 on 2020-04-30 23:17

import common.get_file_path
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_merge_20200427_1615'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActionUserRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('action', models.CharField(choices=[(1, 'Follow'), (2, 'UnFollow')], default=1, max_length=255)),
            ],
            options={
                'ordering': ['-created_at', '-updated_at'],
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='followuser',
            name='follower',
        ),
        migrations.RemoveField(
            model_name='followuser',
            name='following',
        ),
        migrations.AlterField(
            model_name='person',
            name='profile_image',
            field=models.ImageField(blank=True, help_text='If you are company,enter company icon.', null=True, upload_to=common.get_file_path.get_profile_image_path),
        ),
        migrations.DeleteModel(
            name='FollowUser',
        ),
        migrations.AddField(
            model_name='actionuserrelation',
            name='action_by_person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='action_by_person', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='actionuserrelation',
            name='action_on_person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='action_on_person', to=settings.AUTH_USER_MODEL),
        ),
    ]
