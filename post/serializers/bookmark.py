from rest_framework import serializers
from post.models.bookmark import Bookmark
from users.serializers.profile import ProfileViewSerializer
from post.serializers.post import Postserializer


class Bookmarkserializer(serializers.ModelSerializer):
    author = ProfileViewSerializer(read_only=True)
    post = Postserializer(read_only=True)
    createdAt = serializers.SerializerMethodField(method_name='get_created_at')
    updatedAt = serializers.SerializerMethodField(method_name='get_updated_at')

    class Meta:
        model = Bookmark
        fields = (
            'author',
            'createdAt',
            'post',
            'updatedAt',
        )

    def create(self, validated_data):
        author = self.context.get('author', None)
        post = self.context.get('post', None)
        bookmark = Bookmark.objects.create(
            author=author, post=post, **validated_data)

        return bookmark

    def get_created_at(self, instance):
        return instance.created_at.isoformat()

    def get_updated_at(self, instance):
        return instance.updated_at.isoformat()
