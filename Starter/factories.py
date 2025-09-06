import factory
from tracker.models import Transaction, Category, User

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User  # Replace with your actual User model
        django_get_or_create = ('username',)
    


    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    username = factory.Sequence(lambda n: f'user{n}')

    