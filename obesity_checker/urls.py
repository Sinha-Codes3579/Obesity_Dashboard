"""
URL configuration for obesity_checker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from subscriptions.views import home, lifestyle_test_api, symptoms_test_api, lipid_test_view, health_status_view, upload_document # Import home view


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", home, name="home"),  # Homepage
    path("subscriptions/", include("subscriptions.urls")),
    path("accounts/", include("allauth.urls")),
    path('api/lifestyle-test/', lifestyle_test_api, name='lifestyle_test_api'),
    path('api/symptoms-test/', symptoms_test_api, name='symptoms_test_api'),
    path('api/lipid_test/', lipid_test_view, name='lipid_test_view'),
    path("health_status/", health_status_view, name="health_status"),
    path("upload-document/", upload_document, name="upload_document"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
