from django.urls import path
from .views import *


urlpatterns = [
    path('refbooks/', CatalogViewSet.as_view({'get': 'list'}), name='catalog'),
    path('refbooks/<uuid:id_>/elements/', ElementCatalogViewSet.as_view({'get': 'list'}), name='catalog_elements'),
    path('refbooks/<uuid:id_>/check-element/', CheckElementViewSet.as_view({'get': 'check_element'}), name='check_element'),
]