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
from django.conf.urls import url
from products import views
from rest_framework import routers
from rest_framework.documentation import include_docs_urls

router = routers.SimpleRouter()

router.register(r'api/products', views.ProductViewSet)
router.register(r'api/groups', views.ProductViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api/docs/', include_docs_urls(title='Product Service API')),
]

urlpatterns += router.urls