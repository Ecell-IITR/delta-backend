from rest_framework import serializers

from utilities.models import Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        exclude = ('id', 'created_at', 'updated_at',)
