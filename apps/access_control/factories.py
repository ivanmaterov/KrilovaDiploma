from factory.django import DjangoModelFactory
from factory import Faker
from factory.fuzzy import FuzzyChoice
from apps.access_control.models import AccessControl


class AccessControlFactory(DjangoModelFactory):
    # use `bban` to generate specific strings
    # https://faker.readthedocs.io/en/master/providers/faker.providers.bank.html#faker.providers.bank.Provider.bban  # noqa
    computer_name = Faker('bban')
    username = Faker('user_name')
    device_display_name = Faker('bban')
    device_system_name = Faker('name')
    device_serial_id = Faker('aba')
    soi_id = Faker('license_plate')
    sadd_id = Faker('license_plate')
    status = FuzzyChoice(choices=AccessControl.StatusChoices.values)

    class Meta:
        model = AccessControl
