from rest_framework import serializers
from users.models import SocialLink


class SocialLinkSerializers(serializers.ModelSerializer):
    class Meta:
        model = SocialLink
        fields = "__all__"

