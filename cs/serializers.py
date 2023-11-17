from rest_framework.serializers import ModelSerializer

from cs.models import Feedback


class FeedbackSerializer(ModelSerializer):
    class Meta:
        model = Feedback
        fields = ("content",)
