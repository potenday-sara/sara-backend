from __future__ import absolute_import, unicode_literals

from celery import shared_task
from django.conf import settings
from django.utils import timezone
from slack import WebClient
from slack.errors import SlackApiError

from answers.models import Answer
from questions.models import Question
from questions.models.ai_models import AIType
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


@shared_task
def task_send_slack_message():
    client = WebClient(token=settings.SLACK_TOKEN)

    text_format = """
    📅 *Daily*
    
    • *기간* : `{}` ~ `현재`
        • *전체 질문 수* : `{}`
        • *사라 질문 수* : `{}`
        • *마라 질문 수* : `{}`
        
    • *누적 데이터*
        • *전체 질문 수* : `{}`
        • *사라 질문 수* : `{}`
        • *마라 질문 수* : `{}`
    """

    now = timezone.now()
    d_1 = timezone.now() - timezone.timedelta(days=1)
    daily_all_count = Question.objects.filter(created_at__range=(d_1, now)).count()
    daily_sara_count = Question.objects.filter(
        created_at__range=(d_1, now), type=AIType.SARA
    ).count()
    daily_mara_count = Question.objects.filter(
        created_at__range=(d_1, now), type=AIType.MARA
    ).count()

    all_count = Question.objects.all().count()
    sara_count = Question.objects.filter(type=AIType.SARA).count()
    mara_count = Question.objects.filter(type=AIType.MARA).count()

    text = text_format.format(
        d_1.strftime("%Y-%m-%d"),
        daily_all_count,
        daily_sara_count,
        daily_mara_count,
        all_count,
        sara_count,
        mara_count,
    )

    try:
        client.chat_postMessage(channel="#데일리사용량", text=text)
    except SlackApiError as e:
        print(f"Error sending message: {e.response['error']}")
