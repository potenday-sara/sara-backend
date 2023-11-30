from unittest.mock import patch

from django.conf import settings
from django.test import TestCase

from questions.models import AI
from questions.services import GPTService
from questions.tests.factories import AIFactory


class GPTService_테스트(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.ai = AIFactory(type="sara")

    def test_인스턴스_생성_시(self):
        gpt_service = GPTService(self.ai.type)
        with self.subTest("model이 정상적으로 설정된다."):
            self.assertEqual(gpt_service.model, settings.OPENAI_MODEL)

        with self.subTest("role이 정상적으로 설정된다."):
            self.assertEqual(gpt_service.role["role"], "system")
            self.assertEqual(gpt_service.role["content"], self.ai.instruction)

        with self.subTest("message_template이 정상적으로 설정된다."):
            self.assertEqual(
                gpt_service.message_template,
                "[구매 조언 요청 형식]\n상품:%s\n고민하고 있는 이유:%s",
            )
        with self.subTest("client가 정상적으로 설정된다."):
            self.assertIsNotNone(gpt_service.client)

        with self.subTest("존재하지 않는 AI 타입이 들어오면 에러가 발생한다."):
            with self.assertRaises(AI.DoesNotExist):
                GPTService("nonexistent_type")

    @patch("questions.services.OpenAI")
    def test_get_answer_성공_시(self, mock_openai):
        mock_openai.return_value.chat.completions.create.return_value = (
            mock_openai.return_value.chat.completions.create.return_value
        )
        mock_openai.return_value.chat.completions.create.return_value.choices = [
            mock_openai.return_value.chat.completions.create.return_value.choices[0]
        ]
        mock_openai.return_value.chat.completions.create.return_value.choices[
            0
        ].message.content = "테스트 답변"
        gpt_service = GPTService(self.ai.type)
        answer = gpt_service.get_answer("테스트 상품", "테스트 질문")

        with self.subTest("답변이 정상적으로 생성된다."):
            self.assertEqual(answer, "테스트 답변")
