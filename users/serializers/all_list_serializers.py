from rest_framework import serializers

from common.field_choices import USER_FIELD_CHOICES

from users.models import Company
from users.serializers import PersonSerializer

class OrganizationListSerializer(serializers.ModelSerializer):
  person = PersonSerializer()
  is_follow  = serializers.SerializerMethodField()
  followers_count = serializers.SerializerMethodField()

  class Meta:
    model = Company
    fields = '__all__'

  def get_is_follow(self, obj):
    person = self.context.get('person') or None
    return obj.person.action_on_person.filter(
            action_by_person=person, action=USER_FIELD_CHOICES.FOLLOW).exists()
  
  def get_followers_count(self, obj):
    return obj.person.action_on_person.filter(action=USER_FIELD_CHOICES.FOLLOW).count()