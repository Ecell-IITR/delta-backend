from rest_framework import serializers

from users.serializers import PersonSerializer

from post.models import Competition
from utilities.serializers import TagSerializer


class CompetitionSerializer(serializers.ModelSerializer):

    user = PersonSerializer(
        read_only=True
    )
    tags = TagSerializer(many=True)
    # bookmark = serializers.SerializerMethodField('is_bookmark')

    class Meta:
        model = Competition
        exclude = ['bookmarks']

    # def is_bookmark(self, obj):
    #     person = self.context['request'].user
    #     starred_posts = obj.bookmarks.all()

    #     return starred_posts.filter(person=person).exists()
