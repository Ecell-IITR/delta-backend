from rest_framework import serializers
from users.serializers import PersonSerializer
from post.models import Project


class ProjectSerializer(serializers.ModelSerializer):

    user = PersonSerializer(
        read_only=True
    )

    bookmark = serializers.SerializerMethodField('is_bookmark')

    class Meta:
        model = Project
        exclude = ['bookmarks']

    def is_bookmark(self, obj):
        person = self.context['request'].user
        starred_posts = obj.bookmarks.all()

        return starred_posts.filter(person=person).exists()

    def create(self, validated_data):

        user = self.context.get('user', None)

        project = Project.objects.create(
            user=user, **validated_data
        )

        return project
