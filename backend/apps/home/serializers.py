from rest_framework import serializers
from .models import LsClaimList, LsEventList, ClOap, ClPersonList


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


class PersonsClaimsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LsClaimList
        fields = ['idclaim', 'claim_number']


class ClPersonListSerializer(serializers.ModelSerializer):
    claims = PersonsClaimsSerializer(many=True, read_only=True)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['total_claims'] = len(ret['claims'])
        return ret

    class Meta:
        model = ClPersonList
        fields = ['claims', 'full_name']
        depth = 2
