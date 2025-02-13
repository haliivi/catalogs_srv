import uuid
from django.db import models

__all__ = ['Catalog', 'VersionCatalog', 'ElementCatalog']


class BaseModel(models.Model):
    """Base model"""
    objects = models.Manager()

    id = models.UUIDField(verbose_name='Идентификатор', primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        abstract = True

class Catalog(BaseModel):
    """Модель справочников"""

    code = models.CharField(verbose_name='Код', max_length=100, unique=True)
    name = models.CharField(verbose_name='Наименование', max_length=300)
    description = models.TextField(verbose_name='Описание', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Справочник'
        verbose_name_plural = 'Справочники'

class VersionCatalog(BaseModel):
    """Модель версий справочников"""

    catalog = models.ForeignKey(Catalog, verbose_name='Идентификатор справочника', on_delete=models.CASCADE)
    version = models.CharField(verbose_name='Версия', max_length=50)
    date_start_actual = models.DateField(verbose_name='Дата начала действия версии', blank=True, null=True)

    def __str__(self):
        return self.version

    class Meta:
        verbose_name = 'Версия справочника'
        verbose_name_plural = 'Версии справочника'
        constraints = [
            models.UniqueConstraint(
                fields=['catalog', 'version'],
                name='unique_version_by_catalog'
            ),
            models.UniqueConstraint(
                fields=['catalog', 'date_start_actual'],
                name='unique_start_date_by_catalog',
            ),
        ]

class ElementCatalog(BaseModel):
    """Модель элементов справочника"""

    version_catalog = models.ForeignKey(VersionCatalog, verbose_name='Идентификатор версии справочника', on_delete=models.CASCADE)
    code = models.CharField(verbose_name='Код элемента', max_length=100)
    value = models.CharField(verbose_name='Значение элемента', max_length=300)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'Элемент справочника'
        verbose_name_plural = 'Элементы справочника'
        constraints = [
            models.UniqueConstraint(
                fields=['version_catalog', 'code'],
                name='unique_element_code_per_by_version'
            )
        ]
