from django.test import TestCase
from pony_indice import models
from pony_indice import querysets
from pony_indice.tests import factories


class LinkQuerySetTest(TestCase):
    def setUp(self):
        self.link = factories.LinkFactory.create()

    def test_filter_q_on_display(self):
        qs = models.Link.objects.filter_q(self.link.display[:10])
        self.assertTrue(qs.exists())

    def test_filter_q_not_found(self):
        qs = models.Link.objects.filter_q('FOO')
        self.assertFalse(qs.exists())


class DefaultFilterQTest(TestCase):
    def setUp(self):
        self.link = factories.LinkFactory.create()
        self.qs = models.Link.objects.all()

    def test_on_display(self):
        qs = querysets.default_filter_q(self.qs, self.link.display[:10])
        self.assertTrue(qs.exists())

    def test_on_description(self):
        qs = querysets.default_filter_q(self.qs, self.link.description[:10])
        self.assertTrue(qs.exists())

    def test_on_tags(self):
        qs = querysets.default_filter_q(self.qs, self.link.tags[:10])
        self.assertTrue(qs.exists())

    def test_not_found(self):
        qs = querysets.default_filter_q(self.qs, 'FOO')
        self.assertFalse(qs.exists())
