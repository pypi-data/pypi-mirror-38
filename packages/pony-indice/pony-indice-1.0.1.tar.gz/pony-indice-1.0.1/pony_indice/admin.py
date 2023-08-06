from django.contrib import admin
from django.template import defaultfilters
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.urls import reverse
from pony_indice import models
from pony_indice import settings


class FirstLetterFilter(admin.SimpleListFilter):
    title = _('first letter')
    parameter_name = 'first_letter'

    def lookups(self, request, model_admin):
        return [
            (chr(i), chr(i).upper())
            for i in range(97, 123)
        ]

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            return queryset.filter(display__startswith=value)


@admin.register(models.Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('display', 'get_url_display', 'rank', 'get_tags_display', 'removed')
    list_filter = ('removed', FirstLetterFilter,)
    list_per_page = 500
    search_fields = ('display', 'description', 'tags')
    ordering = settings.DEFAULT_ORDER_BY
    read_only_fields = ('url',)
    list_editable = ('rank', 'removed',)
    save_on_top = True

    fields = (
        ('display', 'url',),
        ('rank', 'removed',),
        ('tags', 'description',),
    )

    def get_url_display(self, instance):
        """Helper to show URLs as <a> tag."""
        display = defaultfilters.truncatechars(instance.url, 50)
        tag = '<a href="%s">%s</a>' % (instance.url, display)
        return mark_safe(tag)
    get_url_display.short_description = _("URL")

    def get_tags_display(self, instance):
        tags = []
        for tag in instance.tags.split():
            tag = '<a href="%s">%s</a>' % (
                '%s?q=%s' % (reverse('admin:pony_indice_link_changelist'), tag),
                tag
            )
            tags.append(tag)
        tags = mark_safe(' '.join(tags))
        return tags
    get_tags_display.short_description = _("Tags")
