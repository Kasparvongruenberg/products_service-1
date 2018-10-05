from rest_framework import serializers
from . import models


class ProducstSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Product
        fields = '__all__'


class PropertySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Property
        fields = '__all__'
