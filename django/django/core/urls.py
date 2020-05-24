from django.contrib import admin
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles import views

urlpatterns = [
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    if settings.DEBUG:
        urlpatterns += static(
            settings.MEDIA_URL,
            document_root=settings.MEDIA_ROOT
        )
    urlpatterns += [
        re_path(
            r'^static/(?P<path>.*)$',
            views.serve
        ),
    ]

