from django.db.models import signals
from django.template.defaultfilters import capfirst
from pony_indice import models
from pony_indice import utils


def link_update(sender, instance, **kwargs):
    """
    Receiver for create or update a link.
    """
    from pony_indice.registry import registry

    model_class = instance._meta.model
    options = registry.get_model_options(model_class)
    if model_class not in registry.models:
        return
    utils.create_or_update_link(instance, model_class, options)


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
