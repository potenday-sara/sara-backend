from rest_framework.serializers import ModelSerializer

from answers.models import Answer


class AnswerSerializer(ModelSerializer):
    class Meta:
        model = Answer
        fields = (
            "id",
            "content",
        )
