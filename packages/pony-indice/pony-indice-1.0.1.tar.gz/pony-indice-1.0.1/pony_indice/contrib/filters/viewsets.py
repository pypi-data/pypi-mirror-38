from django_filters import rest_framework as filters
from pony_indice.contrib.filters import filtersets
from pony_indice.contrib.rest_framework import viewsets
from pony_indice import models


class FiltersLinkViewSet(viewsets.LinkViewSet):
    filter_backends = (filters.DjangoFilterBackend,)
    # TODO: Remove filter_class for v2
    filterset_class = filter_class = filtersets.LinkFilterSet

    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)
