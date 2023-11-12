from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from questions.models import Question


class QuestionSerializer(ModelSerializer):
    answer = serializers.CharField(source="answer.content", read_only=True)

    class Meta:
        model = Question
        fields = (
            "id",
            "content",
            "product",
            "type",
            "answer",
        )
