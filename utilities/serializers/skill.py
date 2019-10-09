from rest_framework import serializers

from utilities.models import Skill


class SkillSerializer (serializers.ModelSerializer):
    class Meta:
        model = Skill
        field = '__all__'
