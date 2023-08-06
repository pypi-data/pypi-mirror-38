from rest_framework.test import APITestCase
from rest_framework.reverse import reverse_lazy as reverse

from pony_indice.tests import factories


class LinkViewSetTest(APITestCase):
    url = reverse('testapp:link-list')

    def test_get(self):
        factories.LinkFactory.create()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)


class FilteredLinkViewSetMixin:
    def test_get_filter_q(self):
        link = factories.LinkFactory.create()
        params = {'q': link.display}
        response = self.client.get(self.url, data=params)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_get_filter_q_unfound(self):
        link = factories.LinkFactory.create()
        params = {'q': 'FOO'}
        response = self.client.get(self.url, data=params)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 0)


class SimpleFilteredLinkViewSetTest(FilteredLinkViewSetMixin, LinkViewSetTest):
    url = reverse('testapp:simple-filtered-link-list')


class FiltersLinkViewSetTest(FilteredLinkViewSetMixin, LinkViewSetTest):
    url = reverse('testapp:filters-link-list')
