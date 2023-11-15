import factory

from questions.models import Question


class QuestionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Question

    content = factory.Faker("sentence")
    product = factory.Faker("sentence")
