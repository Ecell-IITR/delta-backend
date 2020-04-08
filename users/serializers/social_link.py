from rest_framework import serializers
from users.models import SocialLink
from utilities.serializers import WebsiteSerializer


class SocialLinkSerializer(serializers.ModelSerializer):
    website = WebsiteSerializer()

    class Meta:
        model = SocialLink
        fields = "__all__"
