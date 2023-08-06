from django.contrib import admin
from pony_indice.tests.testproject.testapp import models


@admin.register(models.TestModel)
class TestModelAdmin(admin.ModelAdmin):
    pass


@admin.register(models.CustomCallableModel)
class CustomCallableModelAdmin(admin.ModelAdmin):
    pass
