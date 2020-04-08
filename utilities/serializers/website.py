from rest_framework import serializers

from utilities.models import Website


class WebsiteSerializer (serializers.ModelSerializer):
    class Meta:
        model = Website
        exclude = ('created_at', 'updated_at', )
