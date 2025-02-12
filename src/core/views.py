from django.db.models import OuterRef, Subquery
from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets, response
from .models import Catalog, VersionCatalog, ElementCatalog
from .serializers import *

__all__ = ['CatalogViewSet', 'ElementCatalogViewSet', 'CheckElementViewSet']


class BaseViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        root_key = kwargs.get('root_key')
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return response.Response({root_key: serializer.data})


class CatalogViewSet(BaseViewSet):
    serializer_class = CatalogSerializer

    def get_queryset(self):
        queryset = Catalog.objects.all()
        date = self.request.query_params.get('date')
        if date:
            queryset_last_version = VersionCatalog.objects.filter(
                catalog=OuterRef('pk'),
                date_start_actual__lte=date
            ).order_by('-date_start_actual').values('pk')[:1]
            queryset = queryset.filter(versioncatalog__id=Subquery(queryset_last_version))
        return queryset

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, root_key='refbooks', **kwargs)


class ElementCatalogViewSet(viewsets.ModelViewSet):
    serializer_class = ElementCatalogSerializer

    def get_queryset(self, *args, **kwargs):
        catalog_id = self.kwargs.get('id_')
        catalog = get_object_or_404(Catalog, id=catalog_id)
        version_param = self.request.query_params.get('version')
        queryset = ElementCatalog.objects.filter(
            version_catalog__catalog=catalog,
            version_catalog__version=version_param
        )
        return queryset

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, root_key='elements', **kwargs)


class CheckElementViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        catalog_id = self.kwargs.get('id_')
        catalog = get_object_or_404(Catalog, id=catalog_id)
        code, value = map(lambda key: self.request.query_params.get(key), ('code', 'value'))
        return ElementCatalog.objects.filter(code=code, value=value, version_catalog__catalog=catalog)

    def check_element(self, *args, **kwargs):
        queryset = self.get_queryset()
        return response.Response(
            {
                'valid': True,
                'message': "Элемент с такими параметрами существует в справочнике."
            } if queryset else
            {
                'valid': False,
                'message': 'Элемент с такими параметрами не существует в справочнике.'
            }
        )
