from django.test import TestCase
from pony_indice import registry
from pony_indice.models import Link
from pony_indice.tests.testproject.testapp.models import TestModel


class LinkCreateReceiverTest(TestCase):
    def test_link_create(self):
        instance = TestModel.objects.create(rank=1)
        link = Link.objects.first()
        self.assertIsNotNone(link)
        self.assertIn(str(instance), link.display)
        self.assertEqual(instance.get_absolute_url(), link.url)


class LinkDeleteReceiverTest(TestCase):
    def setUp(self):
        self.instance = TestModel.objects.create(rank=1)
        self.link = Link.objects.first()

    def test_link_delete(self):
        self.instance.delete()
        link_exists = Link.objects.filter(id=self.link.id).exists()
        self.assertFalse(link_exists)
