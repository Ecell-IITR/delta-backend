from rest_framework import serializers
from users.models import FollowUser


class FollowUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowUser
        fields = "__all__"
