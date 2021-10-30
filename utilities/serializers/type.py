
from rest_framework import serializers

from utilities.models import Type


class TypeSerializer (serializers.ModelSerializer):
    class Meta:
        model = Type
        exclude = ('id', 'created_at', 'updated_at')
        
