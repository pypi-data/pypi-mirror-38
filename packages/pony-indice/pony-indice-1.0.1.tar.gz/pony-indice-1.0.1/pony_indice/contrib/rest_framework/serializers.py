from rest_framework import serializers
from pony_indice import models


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Link
        exclude = ()
