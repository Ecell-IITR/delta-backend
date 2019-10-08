from rest_framework import serializers

from users.serializers import PersonSerializer

from post.models import Competition


class CompetitionSerializer(serializers.ModelSerializer):

    user = PersonSerializer(
        read_only=True
    )

    class Meta:
        model = Competition
        fields = '__all__'

    def create(self, validated_data):

        user = self.context.get('user', None)

        competition = Competition.objects.create(
            user=user, **validated_data
        )

        return competition
