from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from core.serializers import RequestSerializer
from questions.models import Comment, Feedback, Question, QuestionFeedback


class QuestionListRequestParamsSerializer(RequestSerializer):
    order = serializers.ChoiceField(
        choices=[("time", "time"), ("like", "like")],
        default="time",
    )
    type = serializers.ChoiceField(
        choices=[("all", "all"), ("sara", "sara"), ("mara", "mara")],
        default="all",
    )
    language = serializers.ChoiceField(
        choices=[("all", "all"), ("KO", "KO"), ("JA", "JA"), ("EN", "EN")],
        default="KO",
    )


class QuestionSerializer(ModelSerializer):
    answer = serializers.PrimaryKeyRelatedField(read_only=True)
    like_count = serializers.IntegerField(read_only=True)
    comment_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Question
        fields = (
            "id",
            "content",
            "product",
            "type",
            "answer",
            "like_count",
            "comment_count",
            "created_at",
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


class FeedbackSerializer(ModelSerializer):
    class Meta:
        model = Feedback
        fields = ("content",)


class QuestionDateCountSerializer(ModelSerializer):
    date = serializers.DateTimeField(format="%Y-%m-%d")
    count = serializers.IntegerField()

    class Meta:
        model = Feedback
        fields = (
            "date",
            "count",
        )


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            "id",
            "content",
            "nickname",
        )
