from django.contrib import admin
from .models import Product, Property


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'create_date', 'edit_date')
    display = 'Product'
    list_filter = ('create_date',)
    search_fields = ('name',)


class PropertyAdmin(admin.ModelAdmin):
    list_display = ('name', 'create_date', 'edit_date')
    display = 'Property'
    list_filter = ('create_date',)
    search_fields = ('name',)


admin.site.register(Product, ProductAdmin)
admin.site.register(Property, PropertyAdmin)
