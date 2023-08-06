from election.models import ElectionEvent
from rest_framework import serializers


class ElectionEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectionEvent
        fields = "__all__"
