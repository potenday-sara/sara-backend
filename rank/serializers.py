from rest_framework import serializers

from questions.models.ai_models import AIType


class RankSerializer(serializers.Serializer):
    type = serializers.ChoiceField(write_only=True, choices=AIType.choices)
    product = serializers.CharField(read_only=True)
    rank = serializers.IntegerField(read_only=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
