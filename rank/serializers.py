from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from questions.models import Question
from questions.models.ai_models import AIType, LanguageType


class RankSerializer(ModelSerializer):
    type = serializers.ChoiceField(write_only=True, choices=AIType.choices)
    language = serializers.ChoiceField(write_only=True, choices=LanguageType.choices)
    product = serializers.CharField(read_only=True)
    rank = serializers.IntegerField(read_only=True)

    class Meta:
        model = Question
        fields = (
            "type",
            "language"
            "product",
            "rank",
        )
