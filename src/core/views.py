import datetime
from django.db.models import Subquery
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, viewsets, response
from rest_framework.exceptions import ValidationError
from .models import *
from .serializers import *
from .utils import get_last_version_catalog


__all__ = ['CatalogViewSet', 'ElementCatalogViewSet', 'CheckElementViewSet']



class BaseViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    http_method_names = ['get']

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
            try:
                date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
            except ValueError:
                raise ValidationError({'error': "Не верный формат даты. Ожидаемый формат: YYYY-MM-DD."})
            queryset_last_versions = VersionCatalog.objects.filter(
                date_start_actual__lte=date
            ).order_by('-date_start_actual').values('pk')
            queryset = queryset.filter(versioncatalog__in=Subquery(queryset_last_versions)).distinct()
        return queryset

    @swagger_auto_schema(
        operation_description='Получение списка справочников',
        manual_parameters=[
            openapi.Parameter(name='date', in_=openapi.IN_QUERY, description='Фильтр по дате', type=openapi.TYPE_STRING)
        ],
        responses={200: CatalogSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, root_key='refbooks', **kwargs)


class ElementCatalogViewSet(BaseViewSet):
    serializer_class = ElementCatalogSerializer

    def get_queryset(self, *args, **kwargs):
        catalog_id = self.kwargs.get('id_')
        catalog = get_object_or_404(Catalog, id=catalog_id)
        version_param = self.request.query_params.get('version')
        queryset = ElementCatalog.objects.all()
        if version_param:
            queryset = queryset.filter(
                version_catalog__catalog=catalog,
                version_catalog__version=version_param
            )
        else:
            last_version_catalog = get_last_version_catalog(catalog=catalog)
            queryset = queryset.filter(version_catalog=Subquery(last_version_catalog))
        return queryset

    @swagger_auto_schema(
        operation_description='Получение элементов заданного справочника',
        manual_parameters=[
            openapi.Parameter(name='version', in_=openapi.IN_QUERY, description='Фильтр по версии', type=openapi.TYPE_STRING)
        ],
        responses={200: ElementCatalogSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, root_key='elements', **kwargs)


class CheckElementViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        catalog_id = self.kwargs.get('id_')
        catalog = get_object_or_404(Catalog, id=catalog_id)
        code, value, version = map(lambda key: self.request.query_params.get(key), ('code', 'value', 'version'))
        if version:
            return ElementCatalog.objects.filter(code=code, value=value, version_catalog__catalog=catalog, version_catalog__version=version)
        else:
            last_version_catalog = get_last_version_catalog(catalog=catalog)
            return ElementCatalog.objects.filter(code=code, value=value, version_catalog=last_version_catalog)

    @swagger_auto_schema(
        operation_description='Валидация элемента справочника',
        manual_parameters=[
            openapi.Parameter(name='code', in_=openapi.IN_QUERY, description='Код элемента', type=openapi.TYPE_STRING),
            openapi.Parameter(name='value', in_=openapi.IN_QUERY, description='Значение элемента', type=openapi.TYPE_STRING),
            openapi.Parameter(name='version', in_=openapi.IN_QUERY, description='Версия справочника', type=openapi.TYPE_STRING)
        ],
        responses={200: openapi.Response(description='Проверка есть ли такой элемент', schema=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
            'valid': openapi.Schema(type=openapi.TYPE_BOOLEAN),
            'message': openapi.Schema(type=openapi.TYPE_STRING)
        }))}
    )
    def check_element(self, *args, **kwargs):
        is_exists = self.get_queryset().exists()
        return response.Response(
            {
                'valid': is_exists,
                'message': 'Элемент с такими параметрами существует в справочнике.'
                if is_exists else
                'Элемент с такими параметрами не существует в справочнике.'
            }
        )
