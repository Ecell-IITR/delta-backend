from rest_framework import serializers

from users.serializers import PersonSerializer

from post.models import Competition


class CompetitionSerializer(serializers.ModelSerializer):

    user = PersonSerializer(
        read_only=True
    )

    bookmark = serializers.SerializerMethodField('is_bookmark')

    class Meta:
        model = Competition
        exclude = ['bookmarks']

    def is_bookmark(self, obj):
        person = self.context['request'].user
        starred_posts = obj.bookmarks.all()

        return starred_posts.filter(person=person).exists()

    def create(self, validated_data):

        user = self.context.get('user', None)

        competition = Competition.objects.create(
            user=user, **validated_data
        )

        return competition
