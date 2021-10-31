from rest_framework import serializers

from users.serializers import PersonSerializer

from post.models import Project
from post.constants import POST_TYPE

from utilities.serializers import TagSerializer


class ProjectSerializer(serializers.ModelSerializer):

    user = PersonSerializer(read_only=True)
    tags = TagSerializer(many=True)
    post_type = serializers.SerializerMethodField()
    is_bookmark = serializers.SerializerMethodField()

    class Meta:
        model = Project
        exclude = ("bookmarks",)

    @staticmethod
    def get_post_type(obj):
        return POST_TYPE.INTERNSHIP_POST_TYPE

    def get_is_bookmark(self, obj):
        person = self.context["request"].user
        starred_posts = obj.bookmarks.all()
        return starred_posts.filter(person=person).exists()
