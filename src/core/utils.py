import datetime
from .models import VersionCatalog


def get_last_version_catalog(catalog):
    date = datetime.datetime.now().date()
    queryset_last_version = VersionCatalog.objects.filter(
        catalog=catalog,
        date_start_actual__lte=date
    ).order_by('-date_start_actual').values('pk')[:1]
    return queryset_last_version