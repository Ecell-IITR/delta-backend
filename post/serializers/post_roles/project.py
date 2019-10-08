from rest_framework import serializers
from users.serializers import PersonSerializer
from post.models import Project


class ProjectSerializer(serializers.ModelSerializer):

    user = PersonSerializer(
        read_only=True
    )

    class Meta:
        model = Project
        fields = '__all__'

    def create(self, validated_data):

        user = self.context.get('user', None)

        project = Project.objects.create(
            user=user, **validated_data
        )

        return project
