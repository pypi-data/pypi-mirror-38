from django.test import TestCase
from django.urls import reverse_lazy as reverse
from pony_indice.tests.testproject.testapp.models import TestModel
from pony_indice import models
from pony_indice import settings


class IncrementRankViewTest(TestCase):
    url = reverse('redirect-hook')

    def test_increment(self):
        # SetUp
        instance = TestModel.objects.create(rank=1)
        link = models.Link.objects.get(url=instance.get_absolute_url())
        next_url = link.url
        data = {'url': next_url}
        # Test
        response = self.client.get(self.url, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, next_url)
        link.refresh_from_db()
        self.assertEqual(
            link.rank, settings.DEFAULT_RANK + settings.DEFAULT_RANK_INCREMENT)

    def test_no_url(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 400)

    def test_no_link(self):
        data = {'url': '/foo'}
        response = self.client.get(self.url, data=data)
        self.assertEqual(response.status_code, 302)
