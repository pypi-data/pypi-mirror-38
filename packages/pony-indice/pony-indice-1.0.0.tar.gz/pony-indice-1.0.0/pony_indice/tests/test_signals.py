from django.test import TestCase
from django.urls import reverse_lazy as reverse
from pony_indice import registry
from pony_indice.models import Link
from pony_indice.tests.testproject.testapp import models


class LinkCreateReceiverTest(TestCase):
    def test_link_create(self):
        instance = models.TestModel.objects.create(rank=1)
        link = Link.objects.first()
        self.assertIsNotNone(link)
        tags = '%s %s' % (instance._meta.verbose_name, str(instance))
        self.assertIn(str(instance), link.display)
        self.assertEqual(instance.get_absolute_url(), link.url)
        self.assertEqual('', link.description)
        self.assertEqual(tags, link.tags)
        self.assertEqual(10, link.rank)

    def test_link_create_custom_callable_url(self):
        instance = models.CustomCallableModel.objects.create(rank=1)
        url = models.get_absolute_url(instance)
        display = models.get_display(instance)
        description = models.get_description(instance)
        tags = models.get_tags(instance)
        rank = models.get_rank(instance)
        link = Link.objects.first()
        self.assertIsNotNone(link)
        self.assertIn(display, link.display)
        self.assertEqual(url, link.url)
        self.assertEqual(description, link.description)
        self.assertEqual(tags, link.tags)
        self.assertEqual(rank, link.rank)

    def test_link_skip(self):
        instance = models.CustomCallableModel.objects.create(rank=-1)
        url = models.get_absolute_url(instance)
        link = Link.objects.first()
        self.assertIsNone(link)

    def test_link_tag_update(self):
        instance = models.CustomCallableModel.objects.create(rank=1)
        url = models.get_absolute_url(instance)
        link = Link.objects.first()
        tags_before = link.tags
        # Update and look at
        link.tags = 'FOO'
        link.save()
        instance.rank = 10
        instance.save()
        # Check
        new_tags = link.tags.split()
        self.assertIn('FOO', new_tags)
        for tag in new_tags:
            self.assertIn(tag, 'FOO ' + tags_before)

class LinkDeleteReceiverTest(TestCase):
    def setUp(self):
        self.instance = models.TestModel.objects.create(rank=1)
        self.link = Link.objects.first()

    def test_link_delete(self):
        self.instance.delete()
        link_exists = Link.objects.filter(id=self.link.id).exists()
        self.assertFalse(link_exists)
