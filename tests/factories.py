import factory.fuzzy
from factory.django import DjangoModelFactory

from products.models import Product, Purchase
from users.models import User


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Faker("email")
    password = factory.Faker("md5")


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    title = factory.Faker('company')
    cost = factory.Faker("pyint", min_value=50, max_value=150)


class PurchaseFactory(DjangoModelFactory):
    class Meta:
        model = Purchase

    user = factory.SubFactory(UserFactory)
    product = factory.SubFactory(ProductFactory)
    count = factory.Faker("pyint", min_value=1, max_value=5)
    comment = factory.Faker("word")
