from unittest.mock import patch

from django.test import TestCase

from questions.tasks import task_get_answer
from questions.tests.factories import AIFactory


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
