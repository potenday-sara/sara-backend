import factory

from answers.models import Answer
from questions.tests.factories import QuestionFactory


class AnswerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Answer

    content = factory.Faker("sentence")
    question = factory.SubFactory(QuestionFactory)
