from django.conf import settings
from openai import OpenAI

from questions.models import AI


class GPTService:
    MODEL = settings.OPENAI_MODEL

    def __init__(self, ai_type: str, language_type: str):
        self.client = OpenAI()

        self.model = self.MODEL

        self.roles = [
            {
                "role": "system",
                "content": AI.objects.get(
                    type=ai_type, language=language_type
                ).instruction,
            }
        ]
        self.message_template = "[구매 조언 요청 형식]\n상품:%s\n고민하고 있는 이유:%s"

    def get_answer(self, product: str, question: str) -> str:
        message = {
            "role": "user",
            "content": self.message_template % (product, question),
        }
        answer = self.client.chat.completions.create(
            model=self.model,
            messages=self.roles + [message],
        )
        return answer.choices[0].message.content
