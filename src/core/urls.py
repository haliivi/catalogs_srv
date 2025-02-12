from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('refbooks', CatalogViewSet, basename='catalog_list')

urlpatterns = [
    path('', include(router.urls)),
    path('refbooks/<uuid:id_>/elements/', ElementCatalogViewSet.as_view({'get': 'list'}), name='catalog_elements'),
    path('refbooks/<uuid:id_>/check-element/', CheckElementViewSet.as_view({'get': 'check_element'}), name='check_element'),
]