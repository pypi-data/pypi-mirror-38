from django.db import models
from django.utils.translation import ugettext_lazy as _
from pony_indice import querysets
from pony_indice import settings


class AbstractLink(models.Model):
    display = models.CharField(max_length=255, verbose_name=_("display"), db_index=True)
    url = models.TextField(max_length=2000, verbose_name=_("URL"))

    description = models.TextField(max_length=2000, verbose_name=_("description"), default='', blank=True)
    tags = models.TextField(max_length=2000, verbose_name=_("tags"), default='', blank=True)

    removed = models.BooleanField(default=False, verbose_name=_("removed"), db_index=True)
    rank = models.IntegerField(db_index=True, default=settings.DEFAULT_RANK, verbose_name=_("rank"))

    objects = querysets.LinkQuerySet.as_manager()

    class Meta:
        abstract = True


class Link(AbstractLink):
    class Meta:
        app_label = 'pony_indice'
        verbose_name = _("link")
        verbose_name_plural = _("links")
