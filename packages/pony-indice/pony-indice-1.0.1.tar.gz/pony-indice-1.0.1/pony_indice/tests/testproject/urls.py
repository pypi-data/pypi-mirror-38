from django.contrib import admin
from django.urls import path

from rest_framework import routers

from pony_indice import views
from pony_indice.contrib.filters import viewsets as filters_viewsets
from pony_indice.contrib.rest_framework import viewsets as base_viewsets

router = routers.DefaultRouter()
router.register(r'link', base_viewsets.LinkViewSet, base_name='link')
router.register(r'filtered-link', base_viewsets.FilteredLinkViewSet, base_name='simple-filtered-link')
router.register(r'filters-link', filters_viewsets.FiltersLinkViewSet, base_name='filters-link')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('rest/', (router.urls, 'rest', 'testapp')),
    path('redirect-hook', views.IncrementRankView.as_view(), name='redirect-hook'),
]
