from rest_framework import serializers
from users.models import ActionUserRelation


class ActionUserRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActionUserRelation
        fields = "__all__"
