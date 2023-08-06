from rest_framework import viewsets
from pony_indice import models
from pony_indice import settings
from pony_indice.contrib.rest_framework import serializers


class LinkViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.LinkSerializer
    model = models.Link
    queryset = model.objects.all()

    def get_queryset(self):
        qs = super().get_queryset()
        if settings.DEFAULT_ORDER_BY:
            qs = qs.order_by(*settings.DEFAULT_ORDER_BY)
        return qs


class FilteredLinkViewSet(LinkViewSet):
    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.query_params.get('q')
        if q:
            qs = qs.filter_q(q)
        return qs
