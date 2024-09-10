"""coleman URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path, include
from django.contrib import admin
from django.conf import settings
from django.http import HttpResponseRedirect

# Rest API
from rest_framework import routers
from mtasks.serializers import TaskViewSet

router = routers.DefaultRouter()
router.register(r'tasks', TaskViewSet)


urlpatterns = [
    re_path('^api/v1/', include(router.urls)),
    re_path(r'^health/', include('health_check.urls')),
]

if settings.ADMIN:
    urlpatterns = [
        re_path(r'^$', lambda r: HttpResponseRedirect('admin/')),   # Remove this redirect if you add custom views
        path('admin/', admin.site.urls),
    ] + urlpatterns

if settings.GOOGLE_SSO_ENABLED:
    urlpatterns = [
        path(
            "google_sso/", include(
                "django_google_sso.urls",
                namespace="django_google_sso"
            )
        ),
    ] + urlpatterns

admin.site.site_title = admin.site.site_header = settings.SITE_HEADER
admin.site.index_title = settings.INDEX_TITLE
