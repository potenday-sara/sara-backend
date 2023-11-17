import factory

from questions.models import AI, Question


class QuestionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Question

    content = factory.Faker("sentence")
    product = factory.Faker("sentence")


class AIFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AI

    type = factory.Faker("sentence")
    instruction = factory.Faker("sentence")
