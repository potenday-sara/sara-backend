from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from questions.models import Question, QuestionFeedback


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


class QuestionFeedbackSerializer(ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(
        queryset=Question.objects.all(), write_only=True
    )
    feedback = serializers.ChoiceField(
        choices=[(1, "good"), (0, "normal"), (-1, "bad")]
    )

    class Meta:
        model = QuestionFeedback
        fields = (
            "question",
            "feedback",
        )
