from django.test import TransactionTestCase as TestCase
from pony_indice import registry
from pony_indice.tests.testproject.testapp import models


class RegistryTest(TestCase):
    def setUp(self):
        self.registry = registry.Registry()

    def test_register(self):
        self.registry.register_model(models.TestModel)
        self.assertIn(models.TestModel, self.registry.models)


class RegisterTest(TestCase):
    def setUp(self):
        self.default_registry = registry.registry.copy()
        registry.registry.clear()

    def tearDown(self):
        registry.registry.clear()
        registry.registry.update(self.default_registry)

    def test_register(self):
        @registry.register_model()
        class Model(models.TestModel):
            pass
        self.assertIn(Model, registry.registry.models)
