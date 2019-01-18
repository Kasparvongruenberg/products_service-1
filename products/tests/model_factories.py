import factory
from django.contrib.auth.models import User

from ..models import Product, Property


class ProductFactory(factory.DjangoModelFactory):
    workflowlevel2_uuid = factory.Faker('uuid4')
    name = factory.Sequence(lambda x: f"Product #{x}")
    make = factory.Faker('company')
    model = factory.Sequence(lambda x: f"Model #{x}")
    type = factory.Sequence(lambda x: f"Type #{x}")
    status = factory.Iterator(['in stock', 'out of stock'])

    class Meta:
        model = Product


class PropertyFactory(factory.DjangoModelFactory):
    name = factory.Iterator(['color', 'size', 'weight'])
    type = factory.Sequence(lambda x: f"Type #{x}")
    value = factory.Faker('word')

    class Meta:
        model = Property

    @factory.post_generation
    def products(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for product in extracted:
                self.product.add(product)


class UserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = User

    email = 'admin@example.com'
    username = 'admin'
    password = factory.PostGenerationMethodCall('set_password', 'adm1n')

    is_superuser = True
    is_staff = True
    is_active = True
