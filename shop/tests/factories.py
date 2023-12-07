import factory

from shop.models import Category


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    code = factory.Faker("sentence")
    name = factory.Faker("sentence")
