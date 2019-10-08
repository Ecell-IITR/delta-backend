from rest_framework import serializers

from users.serializers import PersonSerializer

from post.models import Internship


class InternshipSerializer(serializers.ModelSerializer):

    user = PersonSerializer(
        read_only=True
    )

    class Meta:
        model = Internship
        fields = '__all__'

    def create(self, validated_data):

        user = self.context.get('user', None)

        internship = Internship.objects.create(
            user=user, **validated_data
        )

        return internship
