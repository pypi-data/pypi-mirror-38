from django.db import models
from django.urls import reverse_lazy as reverse
from pony_indice import registry


@registry.register_model()
class TestModel(models.Model):
    rank = models.IntegerField()

    class Meta:
        verbose_name = "Test Model"

    def __str__(self):
        return '#%d' % (self.rank)

    def get_absolute_url(self):
        return reverse('admin:testapp_testmodel_change',
                       args=[self.id])


def get_absolute_url(instance):
    return reverse('admin:testapp_customcallablemodel_change',
                   args=[instance.id])


def get_display(instance):
    return '#%d#' % (instance.rank)


GET_DESCRIPTION_TEMP = 'This the #%d'
def get_description(instance):
    return GET_DESCRIPTION_TEMP % instance.rank


def get_tags(instance):
    return '%s %s %s' % (instance._meta.verbose_name, chr(instance.rank+97),
                         instance.rank)


def get_rank(instance):
    return instance.rank * 10


def skip(instance):
    return instance.rank < 0


@registry.register_model(get_absolute_url=get_absolute_url,
                         get_display=get_display,
                         get_description=get_description,
                         get_tags=get_tags,
                         get_rank=get_rank,
                         skip=skip)
class CustomCallableModel(models.Model):
    rank = models.IntegerField()

    class Meta:
        verbose_name = "Custom Callable Model"
