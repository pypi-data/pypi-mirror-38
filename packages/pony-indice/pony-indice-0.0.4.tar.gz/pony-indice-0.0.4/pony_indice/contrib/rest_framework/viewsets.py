from rest_framework import viewsets
from pony_indice import models
from pony_indice.contrib.rest_framework import serializers


class LinkViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.LinkSerializer
    model = models.Link
    queryset = model.objects.all()

    def get_queryset(self):
        return self.queryset.filter_q(self.request.GET.get('q', ''))
