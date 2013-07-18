import factory

from django.contrib.auth import models

class UserFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.User
    FACTORY_DJANGO_GET_OR_CREATE = ('username',)

    first_name = 'John'
    last_name = 'Doe'
    username = 'john@example.com'
    password = factory.PostGenerationMethodCall('set_password', 'secret') 
