from rest_framework import serializers

from users.serializers import PersonSerializer

from post.models import Project

from utilities.serializers import TagSerializer

class ProjectSerializer(serializers.ModelSerializer):

    user = PersonSerializer(
        read_only=True
    )
    tags = TagSerializer(many=True)
    # bookmark = serializers.SerializerMethodField('is_bookmark')

    class Meta:
        model = Project
        exclude = ['bookmarks']

    # def is_bookmark(self, obj):
    #     person = self.context['request'].user
    #     starred_posts = obj.bookmarks.all()

    #     return starred_posts.filter(person=person).exists()
