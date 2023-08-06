from django.db import models
from django.urls import reverse_lazy as reverse
from pony_indice import registry


@registry.register()
class TestModel(models.Model):
    rank = models.IntegerField()

    class Meta:
        verbose_name = "Test Model"

    def __str__(self):
        return '#%d' % (self.rank)

    def get_absolute_url(self):
        return reverse('admin:testapp_testmodel_change', args=[self.id])
