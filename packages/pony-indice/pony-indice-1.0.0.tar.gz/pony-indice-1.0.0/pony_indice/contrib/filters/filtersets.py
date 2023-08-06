import django_filters as filters
from django.utils.translation import ugettext_lazy as _
from pony_indice import models


class LinkFilterSet(filters.FilterSet):
    display = filters.CharFilter(
        field_name='display',
        label=_("Display"),
        lookup_expr='icontains')
    description = filters.CharFilter(
        field_name='description',
        label=_("Description"),
        lookup_expr='icontains')
    tags = filters.CharFilter(
        field_name='tags',
        label=_("Tags"),
        lookup_expr='icontains')
    q = filters.CharFilter(
        method='filter_q',
        label=_("Query"))

    class Meta:
        model = models.Link
        fields = {}

    def filter_q(self, queryset, name, value):
        return queryset.filter_q(value)
