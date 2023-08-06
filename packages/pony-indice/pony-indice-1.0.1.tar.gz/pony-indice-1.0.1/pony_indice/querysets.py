import importlib
from django.db import models
from pony_indice import settings


def default_filter_q(queryset, q, **kwargs):
    return queryset.filter(
        models.Q(display__icontains=q) |
        models.Q(description__icontains=q) |
        models.Q(tags__icontains=q)
    )


class LinkQuerySet(models.QuerySet):
    def filter_q(self, q, **kwargs):
        func_path = settings.FILTER_FUNC_PATH
        module_path = '.'.join(func_path.split('.')[:-1])
        func_name = func_path.split('.')[-1]
        module = importlib.import_module(module_path)
        func = getattr(module, func_name)
        return func(self, q, **kwargs)
