import uuid

from django.db import models
from django.utils import timezone


def make_filepath(instance, filename):
    now = timezone.now()
    new_filename = "%s.%s" % (uuid.uuid4(), filename.split('.')[-1])
    filepath = "uploads/%s-%s/%s/" % (now.year, now.month, now.day)
    return filepath+new_filename


class Product(models.Model):
    """
    Model for product
    """
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    workflowlevel2_uuid = models.CharField(max_length=255, verbose_name='WorkflowLevel2 UUID', blank=True, help_text="Unique ID to relate back  to Bifrost workflow")
    name = models.CharField(max_length=255, help_text="Product name")
    make = models.CharField(max_length=255, help_text="Who made the product", blank=True, null=True)
    model = models.CharField(max_length=255, help_text="What is the model from the manufacturer", blank=True, null=True)
    style = models.CharField(max_length=255, help_text="Distinguishing look or color of  product", blank=True, null=True)
    description = models.CharField(max_length=255, help_text="Detailed info", blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True, help_text="Type of product")
    file = models.FileField(upload_to=make_filepath, null=True, blank=True)
    file_name = models.CharField(max_length=50, null=True, blank=True, help_text='Filename')
    status = models.CharField(max_length=255, blank=True, null=True, help_text="Status of Product (in-stock, on back order etc.) ")
    reference_id = models.CharField("Product identifier", max_length=255, blank=True, null=True, help_text="Unique ID for external tracking or thrid part data system")
    create_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} <{}>'.format(self.name, self.type)


class Property(models.Model):
    """
    Model for product's property
    """
    # TODO: Think about making PropertyValue model to store property value for
    #  a certain product
    product = models.ManyToManyField(Product, blank=True)
    name = models.CharField(max_length=255, help_text="Dynamic Field name for additional meta definition of a product")
    type = models.CharField(max_length=255, blank=True, null=True, help_text="Type of field")
    value = models.CharField(max_length=255, help_text="Dynamic Field value for additional meta definition of a product")
    create_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} <{}>'.format(self.name, self.type)
