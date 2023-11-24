from event_services.consumer.services.base import BaseEventService
from questions.models import Answer
from questions.services import GPTService


class QuestionEventService(BaseEventService):
    def execute(self):
        ai_type = self.value["type"]
        product = self.value["product"]
        content = self.value["content"]
        question_id = self.key

        print("gpt answer start")
        gpt_service = GPTService(ai_type=ai_type)
        answer = gpt_service.get_answer(product=product, question=content)
        print(f"gpt answer: {answer}")
        Answer.objects.create(
            question_id=question_id,
            content=answer,
        )
