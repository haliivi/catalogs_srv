from django.contrib import admin
from .models import *


@admin.register(Catalog)
class CatalogAdmin(admin.ModelAdmin):
    pass


@admin.register(VersionCatalog)
class VersionCatalogAdmin(admin.ModelAdmin):
    pass


@admin.register(ElementCatalog)
class ElementCatalogAdmin(admin.ModelAdmin):
    pass
