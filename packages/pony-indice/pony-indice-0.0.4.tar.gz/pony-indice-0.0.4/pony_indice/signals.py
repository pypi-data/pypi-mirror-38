from django.db.models import signals
from django.template.defaultfilters import capfirst
from pony_indice import models


def link_update(sender, instance, **kwargs):
    """
    Receiver for create or update a link.
    """
    from pony_indice.registry import registry

    model_class = instance._meta.model
    if model_class not in registry.models:
        return
    url = instance.get_absolute_url()
    display = '%s : %s' % (capfirst(model_class._meta.verbose_name),
                           str(instance))
    link = models.Link.objects.filter(url=url).first()
    if link is None:
        link = models.Link.objects.create(url=url, display=display)
    link.display = display
    link.url = url
    link.save()


def link_delete(sender, instance, **kwargs):
    """
    Receiver for remove a link.
    """
    from pony_indice.registry import registry

    model_class = instance._meta.model
    if model_class not in registry.models:
        return
    url = instance.get_absolute_url()
    models.Link.objects.filter(url=url).delete()


DJANGO_DB_SIGNALS = [
    (signals.post_save, link_update, 'link_update'),
    (signals.post_delete, link_delete, 'link_delete'),
]
