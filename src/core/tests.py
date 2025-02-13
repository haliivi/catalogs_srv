from datetime import datetime

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase
from .models import *



class CatalogViewSetTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse(viewname='catalog_list')
        catalog_1 = Catalog.objects.create(name='Справочник 1', code='20ОS0J0S')
        VersionCatalog.objects.create(catalog=catalog_1, date_start_actual=datetime(year=2023, month=1, day=15), version='01')
        VersionCatalog.objects.create(catalog=catalog_1, date_start_actual=datetime(year=2023, month=2, day=23), version='02')
        VersionCatalog.objects.create(catalog=catalog_1, date_start_actual=datetime(year=2023, month=10, day=20), version='03')
        catalog_2 = Catalog.objects.create(name='Справочник 2', code='300B0J20')
        VersionCatalog.objects.create(catalog=catalog_2, date_start_actual=datetime(year=2023, month=4, day=9), version='01')
        VersionCatalog.objects.create(catalog=catalog_2, date_start_actual=datetime(year=2023, month=5, day=6), version='02')


    def test_get_catalogs_with_valid_date(self):
        def get_catalog(valid_date, len_list):
            response = self.client.get(path=self.url, data={'date': valid_date})
            data = response.data
            self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
            self.assertIn(member='refbooks', container=data)
            self.assertEqual(first=len(data.get('refbooks')), second=len_list)
        get_catalog(valid_date='2023-01-09', len_list=0)
        get_catalog(valid_date='2023-01-16', len_list=1)
        get_catalog(valid_date='2023-05-05', len_list=2)

    def test_get_catalogs_with_invalid_date(self):
        invalid_date = '2023-01-32'
        response = self.client.get(path=self.url, data={'date': invalid_date})
        self.assertEqual(first=response.status_code, second=status.HTTP_400_BAD_REQUEST)
        self.assertIn(member='error', container=response.data)


class ElementCatalogViewSetTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.catalog_1 = Catalog.objects.create(name='Справочник 1', code='20ОS0J0S')
        self.url = reverse(viewname='catalog_elements', kwargs={'id_': self.catalog_1.id})
        version_catalog_1 = VersionCatalog.objects.create(catalog=self.catalog_1, date_start_actual=datetime(year=2023, month=1, day=15), version='01')
        version_catalog_2 = VersionCatalog.objects.create(catalog=self.catalog_1, date_start_actual=datetime(year=2023, month=2, day=23), version='02')
        version_catalog_3 = VersionCatalog.objects.create(catalog=self.catalog_1, date_start_actual=datetime(year=2023, month=10, day=20), version='03')
        ElementCatalog.objects.create(version_catalog=version_catalog_1, code='A100', value='Element 1')
        ElementCatalog.objects.create(version_catalog=version_catalog_2, code='A123', value='Element 1')
        ElementCatalog.objects.create(version_catalog=version_catalog_3, code='A146', value='Element 1')
        ElementCatalog.objects.create(version_catalog=version_catalog_3, code='A154', value='Element 2')
        ElementCatalog.objects.create(version_catalog=version_catalog_3, code='A178', value='Element 3')

    def test_get_elements_with_version(self):
        response = self.client.get(path= self.url, data={'version': '03'})
        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        self.assertIn(member='elements', container=response.data)

    def test_get_elements_without_version(self):
        response = self.client.get(path=self.url)
        print(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('elements', response.data)
