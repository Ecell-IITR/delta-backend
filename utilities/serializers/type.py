
from rest_framework import serializers

from utilities.models import Skill


class TypeSerializer (serializers.ModelSerializer):
    class Meta:
        model = Skill
        exclude = ('id', 'created_at', 'updated_at', 'slug')
        
