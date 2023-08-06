from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from pony_indice import models


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
    list_display = ('display', 'get_url_display', 'removed')
    list_filter = ('removed', FirstLetterFilter,)
    list_per_page = 2000
    search_fields = ('display', 'description')
    ordering = ('display',)
    read_only_fields = ('url',)
    list_editable = ('removed',)

    fields = (
        ('display', 'url', 'removed'),
        ('description',),
    )

    def get_url_display(self, instance):
        """Helper to show URLs as <a> tag."""
        tag = '<a href="%s">%s</a>' % (instance.url, instance.url)
        return mark_safe(tag)
    get_url_display.short_description = _("URL")
