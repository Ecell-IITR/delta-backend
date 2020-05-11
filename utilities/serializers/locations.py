from rest_framework import serializers

from utilities.serializers import StateSerializer, CountrySerializer
from utilities.models import Location


class LocationSerializer (serializers.ModelSerializer):
    country = CountrySerializer()
    state = StateSerializer()
    
    class Meta:
        model = Location
        exclude = ('created_at', 'updated_at')
