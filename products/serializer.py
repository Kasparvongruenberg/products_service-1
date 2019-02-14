from django.urls import reverse

from rest_framework import serializers
from . import models


class ProductSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        # replace direct file link with file entry point URL
        data = super().to_representation(instance)
        data['file'] = reverse('product-file', args=(instance.uuid,)) \
            if data['file'] else None
        return data

    def create(self, validated_data):
        file_data = validated_data['file']
        if file_data and not validated_data['file_name']:
            validated_data['file_name'] = file_data.name
        return super().create(validated_data)

    class Meta:
        model = models.Product
        fields = '__all__'


class PropertySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Property
        fields = '__all__'
