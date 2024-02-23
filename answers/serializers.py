from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from answers.models import Answer


class AnswerSerializer(ModelSerializer):
    product = serializers.CharField(source="question.product")

    class Meta:
        model = Answer
        fields = (
            "id",
            "product",
            "content",
        )
