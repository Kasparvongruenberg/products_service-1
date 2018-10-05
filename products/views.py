from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.pagination import CursorPagination, PageNumberPagination
import django_filters
from . import models as rules
from . import serializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


class SmallResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 50


class DefaultCursorPagination(CursorPagination):
    """
    TODO move this to settings to provide better standardization
    See http://www.django-rest-framework.org/api-guide/pagination/
    """
    page_size = 30
    max_page_size = 100
    page_size_query_param = 'page_size'


class ProductViewSet(viewsets.ModelViewSet):
    """
    Product viewset is used to create list or inventory of products or THINGS to be
    tracked and related to a project
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    # Remove CSRF request verification for posts to this API
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(ProductViewSet, self).dispatch(*args, **kwargs)

    def list(self, request):
        # Use this queryset or the django-filters lib will not work
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    filter_fields = ('type', 'name')
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    queryset = rules.Product.objects.all()
    serializer_class = serializer.ProductSerializer


class PropertyViewSet(viewsets.ModelViewSet):
    """
    A property is a subset of product that can be allocated to provide additional
    meta descriptions about the product
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    def list(self, request):
        # Use this queryset or the django-filters lib will not work
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    filter_fields = ('type', 'prodcut__name', 'name')
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    queryset = rules.Property.objects.all()
    serializer_class = serializer.PropertySerializer
