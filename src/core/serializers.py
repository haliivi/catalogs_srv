from rest_framework import serializers
from .models import *

__all__ = ['CatalogSerializer', 'ElementCatalogSerializer']


class CatalogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catalog
        fields = ['id', 'code', 'name']


class ElementCatalogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElementCatalog
        fields = ['code', 'value']
