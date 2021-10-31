from rest_framework import serializers

from utilities.models import Skill, SkillType


class SkillTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillType
        exclude = ("created_at", "updated_at")


class SkillSerializer(serializers.ModelSerializer):
    type = SkillTypeSerializer()

    class Meta:
        model = Skill
        exclude = ("created_at", "updated_at")
