try:
    import debug_toolbar.urls as dt_urls
except ImportError:
    dt_urls = None

if dt_urls:
    from django.conf.urls import include
    from .urls import urlpatterns

    dt_urls.urlpatterns += [
        ('', include(urlpatterns)),
    ]
