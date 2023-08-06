import faker
import factory
from factory import fuzzy


class LinkFactory(factory.django.DjangoModelFactory):
    display = factory.Faker('sentence')
    url = factory.Faker('url')
    description = factory.Faker('sentence')
    tags = factory.Faker('sentence')

    class Meta:
        model = 'pony_indice.Link'
