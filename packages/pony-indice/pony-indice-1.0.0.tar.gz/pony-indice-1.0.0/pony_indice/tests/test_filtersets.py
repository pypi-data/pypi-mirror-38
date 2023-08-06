from django.test import TestCase
from pony_indice.contrib.filters import filtersets
from pony_indice.tests.testproject.testapp import models


class LinkFilterSetTest(TestCase):
    filterset_class = filtersets.LinkFilterSet

    def setUp(self):
        for i in range(3):
            models.TestModel.objects.create(rank=i)
            models.CustomCallableModel.objects.create(rank=i)

    def test_filter_display(self):
        data = {'display': '0'}
        filterset = self.filterset_class(data=data)
        self.assertEqual(filterset.qs.count(), 2)

    def test_filter_description(self):
        data = {'description': models.GET_DESCRIPTION_TEMP[:5]}
        filterset = self.filterset_class(data=data)
        self.assertEqual(filterset.qs.count(), 3)

    def test_filter_tags(self):
        sample = models.CustomCallableModel.objects.first()
        tags = models.get_tags(sample)
        data = {'tags': tags}
        filterset = self.filterset_class(data=data)
        self.assertEqual(filterset.qs.count(), 1)

    def test_filter_q(self):
        data = {'q': models.GET_DESCRIPTION_TEMP[:5]}
        filterset = self.filterset_class(data=data)
        self.assertEqual(filterset.qs.count(), 3)
