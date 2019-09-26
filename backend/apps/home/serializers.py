from rest_framework import serializers
from .models import LsClaimList, LsEventList, ClOap


class LsEventListSerializer(serializers.ModelSerializer):
    class Meta:
        model = LsEventList
        fields = ['user', 'event_date', 'event_type']
        depth = 5


class ClOapSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClOap
        exclude = ['claims',]
        depth = 5


class ClaimsSerializer(serializers.ModelSerializer):
    events = LsEventListSerializer(many=True, read_only=True)
    oap = ClOapSerializer(many=True, read_only=True)

    class Meta:
        model = LsClaimList
        fields = '__all__'
        depth = 5
