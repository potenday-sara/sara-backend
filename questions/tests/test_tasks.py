from unittest.mock import patch

import freezegun
from django.test import TestCase
from django.utils import timezone
from slack.errors import SlackApiError

from questions.consts import QUESTION_SLACK_MESSAGE_TEMPLATE
from questions.models import Question
from questions.tasks import task_get_answer, task_send_slack_message
from questions.tests.factories import AIFactory, QuestionFactory


class task_get_answer_테스트(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.ai = AIFactory(type="sara")

    @patch("questions.tasks.GPTService")
    @patch("questions.tasks.Answer.objects.create")
    def test_task_get_answer_success(self, mock_create, mock_gpt_service):
        mock_gpt_service.return_value.get_answer.return_value = "테스트 답변"

        # 작업 실행
        task_get_answer(
            "test_key", {"type": "AI", "product": "product1", "content": "질문 내용"}
        )

        # 모의 객체가 예상대로 호출되었는지 확인
        mock_gpt_service.assert_called_once_with(ai_type="AI")
        mock_gpt_service.return_value.get_answer.assert_called_once_with(
            product="product1", question="질문 내용"
        )
        mock_create.assert_called_once_with(question_id="test_key", content="테스트 답변")

    @patch("questions.tasks.GPTService")
    @patch("questions.tasks.print")
    def test_task_get_answer_gpt_service_exception(self, mock_print, mock_gpt_service):
        mock_gpt_service.return_value.get_answer.side_effect = Exception("GPT 서비스 에러")

        task_get_answer(
            "test_key", {"type": "sara", "product": "product1", "content": "질문 내용"}
        )

        mock_print.assert_called_with("gpt error: GPT 서비스 에러")

    @patch("questions.tasks.GPTService")
    @patch("questions.tasks.Answer.objects.create")
    @patch("questions.tasks.print")
    def test_task_get_answer_answer_create_exception(
        self, mock_print, mock_create, mock_gpt_service
    ):
        mock_gpt_service.return_value.get_answer.return_value = "테스트 답변"
        mock_create.side_effect = Exception("Answer 생성 에러")

        task_get_answer(
            "test_key", {"type": "sara", "product": "product1", "content": "질문 내용"}
        )

        mock_print.assert_called_with("answer create error: Answer 생성 에러")


@freezegun.freeze_time("2024-01-01")
class task_send_slack_message_테스트(TestCase):
    @classmethod
    def setUpTestData(cls):
        QuestionFactory.create_batch(10, type="sara")

    @patch("questions.tasks.WebClient")
    def test_task_send_slack_message_success(self, mock_web_client):
        task_send_slack_message()

        now = timezone.now()
        d_1 = now - timezone.timedelta(days=1)
        expect_text = QUESTION_SLACK_MESSAGE_TEMPLATE.format(
            d_1.strftime("%Y-%m-%d"),
            Question.objects.filter(created_at__range=(d_1, now)).count(),
            Question.objects.filter(created_at__range=(d_1, now), type="sara").count(),
            Question.objects.filter(created_at__range=(d_1, now), type="mara").count(),
            Question.objects.all().count(),
            Question.objects.filter(type="sara").count(),
            Question.objects.filter(type="mara").count(),
        )
        mock_web_client.assert_called_once()
        mock_web_client.return_value.chat_postMessage.assert_called_once_with(
            channel="#데일리사용량",
            text=expect_text,
        )

    @patch("questions.tasks.WebClient")
    @patch("questions.tasks.print")
    def test_task_send_slack_message_slack_exception(self, mock_print, mock_web_client):
        error_response = {"ok": False, "error": "invalid_auth"}
        mock_web_client.return_value.chat_postMessage.side_effect = SlackApiError(
            message="Slack API 에러",
            response=error_response,
        )

        task_send_slack_message()

        mock_print.assert_called_with(
            f"Error sending message: {error_response['error']}"
        )
