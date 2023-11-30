from __future__ import absolute_import, unicode_literals

from celery import shared_task

from answers.models import Answer
from questions.services import GPTService


@shared_task
def task_get_answer(key: str, value: dict) -> None:
    ai_type = value["type"]
    product = value["product"]
    content = value["content"]
    question_id = key

    print("gpt answer start")
    try:
        gpt_service = GPTService(ai_type=ai_type)
        answer = gpt_service.get_answer(product=product, question=content)
        print(f"gpt answer: {answer}")
    except Exception as e:  # pylint: disable=broad-except
        print(f"gpt error: {e}")
        return

    try:
        Answer.objects.create(
            question_id=question_id,
            content=answer,
        )
    except Exception as e:  # pylint: disable=broad-except
        print(f"answer create error: {e}")
