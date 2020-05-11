from rest_framework import serializers

from utilities.models import Country


class CountrySerializer (serializers.ModelSerializer):
    class Meta:
        model = Country
        exclude = ('created_at', 'updated_at')
