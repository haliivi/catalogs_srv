from typing import Optional

from django.contrib import admin
from .models import *


class CatalogVersionInline(admin.TabularInline):
    model = VersionCatalog
    extra = 0

class ElementCatalogInline(admin.TabularInline):
    model = ElementCatalog
    extra = 0

@admin.register(Catalog)
class CatalogAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'name', 'get_latest_version', 'get_latest_version_date']
    inlines = [CatalogVersionInline]

    @staticmethod
    def __get_latest_version(obj) -> Optional[VersionCatalog] :
        return obj.versioncatalog_set.order_by('-date_start_actual').first()

    def get_latest_version(self, obj):
        latest_version = self.__get_latest_version(obj)
        return latest_version.version if latest_version else 'нет данных'


    def get_latest_version_date(self, obj):
        latest_version = self.__get_latest_version(obj)
        return latest_version.date_start_actual if latest_version else 'нет данных'

    get_latest_version.short_description = 'Текущая версия'
    get_latest_version_date.short_description = 'Дата начала действия версии'


@admin.register(VersionCatalog)
class VersionCatalogAdmin(admin.ModelAdmin):
    list_display = ['get_catalog_code', 'get_catalog_name', 'version', 'date_start_actual']
    inlines = [ElementCatalogInline]

    def get_catalog_code(self, obj: VersionCatalog):
        return obj.catalog.code


    def get_catalog_name(self, obj: VersionCatalog):
        return obj.catalog.name

    get_catalog_code.short_description = 'Код справочника'
    get_catalog_name.short_description = 'Наименование справочника'


@admin.register(ElementCatalog)
class ElementCatalogAdmin(admin.ModelAdmin):
    pass
