"""products_service URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from products import views
from rest_framework import permissions, routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Products Service API",
        default_version='latest',
        description="Test description",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = routers.SimpleRouter()

router.register(r'products', views.ProductViewSet)
router.register(r'property', views.PropertyViewSet)
router.register(r'groups', views.ProductViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api/docs/swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^api/docs/$', schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'),
    url(r'^api/', include(router.urls))
]
